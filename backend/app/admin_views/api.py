from flask import Blueprint, jsonify
from flask_login import login_required
from database import db

admin_api = Blueprint('admin_api', __name__)

@admin_api.route('/admin/api/series/<int:series_id>/teams')
@login_required
def get_series_teams(series_id):
    """Get teams or players for a series based on its type"""
    # First get series type
    result = db.session.execute("""
        SELECT gt.team_player_amount 
        FROM series s 
        JOIN game_types gt ON s.game_type_id = gt.id 
        WHERE s.id = :series_id
    """, {'series_id': series_id}).first()
    
    if not result:
        return jsonify([])
    
    if result.team_player_amount == 1:
        # For single player series
        teams = db.session.execute("""
            SELECT sr.id, p.name 
            FROM series_registrations sr
            JOIN players p ON sr.contact_player_id = p.id
            WHERE sr.series_id = :series_id
            ORDER BY p.name
        """, {'series_id': series_id}).fetchall()
    else:
        # For team series
        teams = db.session.execute("""
            SELECT sr.id, sr.team_name as name
            FROM series_registrations sr
            WHERE sr.series_id = :series_id
            AND sr.team_name IS NOT NULL
            ORDER BY sr.team_name
        """, {'series_id': series_id}).fetchall()
    
    return jsonify([{'id': str(t.id), 'name': t.name} for t in teams])
