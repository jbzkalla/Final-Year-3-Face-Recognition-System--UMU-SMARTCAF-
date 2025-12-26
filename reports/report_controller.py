from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
from reports.attendance_report import generate_attendance_report, get_attendance_trends, get_meal_distribution
from reports.payment_report import generate_payment_report, get_revenue_trends, get_payment_methods_distribution
from reports.user_activity_report import generate_user_activity_report
from utils.export_utils import generate_excel_with_logo
import io

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/api/reports/attendance', methods=['GET'])
def attendance_report():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    meal = request.args.get('meal')
    dept = request.args.get('department')
    user_id = request.args.get('user_id')
    
    logs = generate_attendance_report(start_date, end_date, meal, dept, user_id)
    trends = get_attendance_trends()
    meals = get_meal_distribution()
    
    return jsonify({
        "success": True,
        "data": {
            "logs": logs,
            "trends": trends,
            "meals": meals
        }
    })

@reports_bp.route('/api/reports/payment', methods=['GET'])
def payment_report():
    report = generate_payment_report()
    revenue_trends = get_revenue_trends()
    methods = get_payment_methods_distribution()
    
    return jsonify({
        "success": True,
        "data": {
            "summary": report['summary'],
            "transactions": report['transactions'],
            "revenue_trends": revenue_trends,
            "methods": methods
        }
    })

@reports_bp.route('/api/reports/activity/<user_id>', methods=['GET'])
def activity_report(user_id):
    report = generate_user_activity_report(user_id)
    if report:
        return jsonify({"success": True, "data": report})
    return jsonify({"success": False, "message": "User not found"}), 404
@reports_bp.route('/api/reports/attendance/export', methods=['GET'])
def export_attendance():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    meal = request.args.get('meal')
    dept = request.args.get('department')
    user_id = request.args.get('user_id')
    
    logs = generate_attendance_report(start_date, end_date, meal, dept, user_id)
    
    headers = ["Date", "User ID", "Name", "Session", "Time", "Status"]
    data_rows = []
    for log in logs:
        data_rows.append([
            log['date'],
            log['id'],
            log['name'],
            log['session'],
            log['time'],
            log['status']
        ])
    
    excel_file = generate_excel_with_logo(data_rows, headers, title="Attendance Report")
    return send_file(
        excel_file,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f"attendance_report_{datetime.now().strftime('%Y%m%d')}.xlsx"
    )

@reports_bp.route('/api/reports/payment/export', methods=['GET'])
def export_payments():
    report = generate_payment_report()
    transactions = report['transactions']
    
    headers = ["Date", "User ID", "Name", "Amount", "Method", "Status", "Description"]
    data_rows = []
    for t in transactions:
        data_rows.append([
            t.get('date', ''),
            t.get('user_id', ''),
            t.get('user_name', ''),
            t.get('amount', ''),
            t.get('method', ''),
            t.get('status', ''),
            t.get('description', '')
        ])
    
    excel_file = generate_excel_with_logo(data_rows, headers, title="Financial Report")
    return send_file(
        excel_file,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f"payment_report_{datetime.now().strftime('%Y%m%d')}.xlsx"
    )

@reports_bp.route('/api/reports/activity/<user_id>/export', methods=['GET'])
def export_activity(user_id):
    report = generate_user_activity_report(user_id)
    if not report:
        return jsonify({"success": False, "message": "User not found"}), 404
        
    logs = report.get('logs', [])
    headers = ["Timestamp", "Activity", "Details"]
    data_rows = []
    for log in logs:
        data_rows.append([
            log.get('timestamp', ''),
            log.get('activity', ''),
            log.get('details', '')
        ])
    
    excel_file = generate_excel_with_logo(data_rows, headers, title=f"Activity Report - {report.get('user_name')}")
    return send_file(
        excel_file,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f"activity_report_{user_id}_{datetime.now().strftime('%Y%m%d')}.xlsx"
    )
