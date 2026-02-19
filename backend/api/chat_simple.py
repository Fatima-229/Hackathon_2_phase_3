from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
import uuid
from uuid import UUID
import json
from database import get_session
from models.user import User
from models.conversation import Conversation, ConversationCreate
from models.message import Message, MessageCreate
from utils.auth import get_current_user
from datetime import datetime
from mcp.server import mcp_server
import os
from openai import OpenAI
from pydantic import BaseModel

router = APIRouter()

# Initialize OpenAI client
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(api_key=api_key)


class ChatRequest(BaseModel):
    user_message: str


@router.post("/{user_id}/chat")
def chat_with_ai(user_id: str, request: ChatRequest, session: Session = Depends(get_session)):
    """
    Main chat endpoint that handles conversation with the AI assistant.
    The AI will use MCP tools to perform task operations.
    """
    try:
        # Verify the user exists and is the same as the authenticated user
        current_user = session.get(User, user_id)
        if not current_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Find or create a conversation for this user
        conversation_query = session.exec(
            select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.created_at.desc())
        ).first()
        if not conversation_query:
            # Create a new conversation
            conversation_data = ConversationCreate()
            conversation_dict = conversation_data.model_dump()
            conversation_dict['user_id'] = user_id
            conversation_dict['id'] = None
            conversation_dict['created_at'] = datetime.utcnow()
            conversation_dict['updated_at'] = datetime.utcnow()

            conversation = Conversation(**conversation_dict)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
        else:
            conversation = conversation_query

        # Save user's message to the conversation
        user_message_db = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=request.user_message,
            created_at=datetime.utcnow()
        )
        session.add(user_message_db)
        session.commit()

        # Prepare messages for the AI, including system prompt
        system_prompt = """You are a helpful AI assistant for managing tasks. You can help users add, list, update, complete, and delete tasks.
        Always use the provided tools to perform these operations. Be friendly and confirm actions with the user.
        The available tools are:
        - add_task: Add a new task with title, description, priority, and due date
        - list_tasks: List tasks with optional filtering by completion status
        - complete_task: Toggle completion status of a task by ID
        - delete_task: Delete a task by ID
        - update_task: Update properties of a task by ID

        Always confirm with the user before performing destructive actions like deleting tasks.
        
        IMPORTANT: You MUST respond to every user message. Even if no tools are needed, acknowledge the message and offer help."""

        # Get recent conversation history (last 10 messages)
        recent_messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.asc())
            .limit(10)
        ).all()

        # Format messages for the AI
        formatted_messages = [{"role": "system", "content": system_prompt}]
        for msg in recent_messages:
            formatted_messages.append({"role": msg.role, "content": msg.content})

        # Add the current user message
        formatted_messages.append({"role": "user", "content": request.user_message})

        try:
            # Get OpenAI client
            client = get_openai_client()

            # Call the OpenAI API with function calling
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=formatted_messages,
                tools=[
                    {
                        "type": "function",
                        "function": mcp_server.get_tool_description("add_task")
                    },
                    {
                        "type": "function",
                        "function": mcp_server.get_tool_description("list_tasks")
                    },
                    {
                        "type": "function",
                        "function": mcp_server.get_tool_description("complete_task")
                    },
                    {
                        "type": "function",
                        "function": mcp_server.get_tool_description("delete_task")
                    },
                    {
                        "type": "function",
                        "function": mcp_server.get_tool_description("update_task")
                    }
                ],
                tool_choice="auto"
            )

            # Process the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                # Process tool calls
                tool_responses = []
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Execute the tool
                    tool_result = mcp_server.execute_tool(function_name, user_id, **function_args)

                    # Add to tool responses
                    tool_responses.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(tool_result)
                    })

                # Get final response from AI with tool results
                final_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=formatted_messages + [response_message] + tool_responses
                )

                ai_response_text = final_response.choices[0].message.content
                tool_calls_result = [tc.function for tc in tool_calls]  # Extract tool calls for response
            else:
                # No tool calls, just return the AI's response
                ai_response_text = response_message.content
                tool_calls_result = []

            # Ensure there's always a response, even if the AI didn't return one
            if not ai_response_text:
                ai_response_text = "I'm here to help you manage your tasks. How can I assist you today?"
                
        except Exception as e:
            # If there's an error with the AI service, return a helpful message
            error_msg = str(e)
            if "OPENAI_API_KEY" in error_msg:
                ai_response_text = "Hi there! I'm your AI task assistant. I can help you manage your tasks like adding, listing, updating, and completing tasks. However, I need to be configured with an OpenAI API key to process your requests. Please contact the administrator to configure the API key."
            else:
                ai_response_text = f"I'm sorry, I encountered an error processing your request: {error_msg}. Could you try rephrasing?"
            tool_calls_result = []

        # Save AI's response to the conversation
        ai_message_db = Message(
            conversation_id=conversation.id,
            user_id=user_id,  # The AI acts on behalf of the user's context
            role="assistant",
            content=ai_response_text,
            created_at=datetime.utcnow()
        )
        session.add(ai_message_db)
        session.commit()

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()

        return {
            "conversation_id": str(conversation.id),
            "response": ai_response_text,
            "tool_calls": tool_calls_result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        # Return error in JSON format to prevent server crashes
        return {"error": str(e)}


@router.get("/{user_id}/chat")
def get_conversations_or_messages(
    user_id: str, 
    conversation_id: Optional[str] = Query(None, description="Specific conversation ID to fetch messages for"),
    session: Session = Depends(get_session)
):
    """
    Get conversation history for a user.
    If conversation_id is provided, returns messages for that conversation.
    If conversation_id is not provided, returns a list of user's conversations.
    """
    # Verify the user exists
    current_user = session.get(User, user_id)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    if conversation_id:
        # Fetch messages for a specific conversation
        conversation_uuid = UUID(conversation_id)
        conversation = session.get(Conversation, conversation_uuid)
        
        if not conversation or str(conversation.user_id) != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found or does not belong to user")
        
        # Get all messages for this conversation
        messages_query = select(Message).where(
            Message.conversation_id == conversation_uuid
        ).order_by(Message.created_at.asc())
        messages = session.exec(messages_query).all()
        
        # Format messages for response
        formatted_messages = [
            {
                "id": str(message.id),
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at.isoformat()
            }
            for message in messages
        ]
        
        return formatted_messages
    else:
        # Fetch list of user's conversations
        conversations_query = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc())
        conversations = session.exec(conversations_query).all()
        
        # Format conversations for response
        formatted_conversations = []
        for conv in conversations:
            # Get the last message for this conversation
            last_message_query = select(Message).where(
                Message.conversation_id == conv.id
            ).order_by(Message.created_at.desc()).limit(1)
            last_message = session.exec(last_message_query).first()
            
            formatted_conversations.append({
                "conversation_id": str(conv.id),
                "last_message": last_message.content if last_message else "",
                "updated_at": conv.updated_at.isoformat()
            })
        
        return formatted_conversations