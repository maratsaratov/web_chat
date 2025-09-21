from flask import Blueprint, request, jsonify
from datetime import datetime
from utils import session_manager
from services import gigachat_service
from gigachat.models import MessagesRole
from config import Config
import logging

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        
        if not data or 'message' not in data:
            return jsonify({
                "success": False,
                "error": "Message is required"
            }), 400
        
        session_id = data.get('session_id')
        if not session_id or not session_manager.get_session(session_id):
            session_id = session_manager.create_session()
        
        session = session_manager.get_session(session_id)
        user_message = data['message']
        session.add_message(MessagesRole.USER, user_message)
        assistant_message = gigachat_service.get_response(session.get_chat_history())
        session.add_message(MessagesRole.ASSISTANT, assistant_message)
        logger.info(f"Session {session_id}: User message processed")
        
        return jsonify({
            "success": True,
            "message": assistant_message,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        })
            
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "session_id": session_id if 'session_id' in locals() else None
        }), 500

@api_bp.route('/session/new', methods=['POST'])
def new_session():
    try:
        session_id = session_manager.create_session()
        return jsonify({
            "success": True,
            "session_id": session_id,
            "created_at": session_manager.get_session(session_id).created_at.isoformat()
        })
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_bp.route('/session/<session_id>', methods=['GET'])
def get_session_info(session_id):
    session = session_manager.get_session(session_id)
    if session:
        return jsonify({
            "success": True,
            "session_id": session_id,
            "message_count": len(session.messages),
            "created_at": session.created_at.isoformat(),
            "last_activity": session.last_activity.isoformat()
        })
    else:
        return jsonify({
            "success": False,
            "error": "Session not found"
        }), 404

@api_bp.route('/session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    try:
        if session_manager.delete_session(session_id):
            return jsonify({
                "success": True,
                "message": "Session deleted"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Session not found"
            }), 404
    except Exception as e:
        logger.error(f"Error deleting session: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_bp.route('/session/<session_id>/clear', methods=['POST'])
def clear_session_history(session_id):
    session = session_manager.get_session(session_id)
    if session:
        session.clear_history()
        return jsonify({
            "success": True,
            "message": "Session history cleared"
        })
    else:
        return jsonify({
            "success": False,
            "error": "Session not found"
        }), 404

@api_bp.route('/health', methods=['GET'])
def health_check():
    try:
        gigachat_connected = gigachat_service.health_check()
        
        return jsonify({
            "status": "healthy" if gigachat_connected else "degraded",
            "gigachat_connected": gigachat_connected,
            "active_sessions": len(session_manager.sessions),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "gigachat_connected": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500