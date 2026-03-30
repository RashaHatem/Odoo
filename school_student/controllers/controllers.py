# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging
import json, sys, traceback
import datetime
from odoo.addons.school_student.tools.methods import *
import jwt

_logger = logging.getLogger(__name__)


def student_profile():
    student = request.env["school.student"].search(
        [("user_id", "=", request.session.uid)], limit=1
    )
    if student:
        return {
            "name": student.name,
            "email": student.email,
            "school_id": student.school_id.name,
            "state_": student.state_,
        }
    return {"note": "No student profile found for the current user"}


class SchoolStudent(http.Controller):

    @http.route("/school_student/school_student", auth="public")
    def index(self, **kw):
        return "Hello, world"

    @http.route(
        "/api/std/login", type="json", auth="none", methods=["POST"], csrf=False
    )
    def login_std(self, **kw):
        try:
            args = request.get_json_data()
            params = args.get("params", {})
            if "login" in params and "password" in params:
                login = params.get("login")
                password = params.get("password")
                db = request.db
                credential = {"login": login, "password": password, "type": "password"}
                result = request.session.authenticate(db, credential)
                uid = result.get("uid")

                if uid:

                    user = request.env["res.users"].sudo().browse(uid)
                    return {
                        "status": "success",
                        "message": f"مرحباً {user.name}، تم تسجيل الدخول بنجاح",
                        "uid": uid,
                        "session_id": request.session.sid,
                    }
                else:
                    return {"status": "error", "message": "User not found"}

            return {"status": "error", "message": "Missing login or password"}

        except Exception as e:

            print("Error in login_std:", str(e))
            return {"status": "error", "message": str(e)}

    @http.route(
        "/rasha/session", type="http", auth="none", methods=["POST"], csrf=False
    )
    def some_uuii(self, **kw):
        try:
            raw_data = request.httprequest.data
            try:
                data = json.loads(raw_data) if raw_data else {}
            except ValueError:
                return "Invalid JSON"

            login = data.get("login")
            password = data.get("password")

            try:
                db = request.db
                credential = {"login": login, "password": password, "type": "password"}
                result = request.session.authenticate(db, credential)
                uid = result.get("uid")
                if uid:
                    user = request.env["res.users"].sudo().browse(uid)
                    response = ApiResponse(
                        message=f"Hello {user.name}",
                        data={"uid": uid, "session_id": request.session.sid},
                    )
                    return response.to_json()
            except Exception as e:

                response = ApiResponse(
                    success=False,
                    message="Missing login or password",
                    status_code=400,
                    error={
                        "type": type(e).__name__,
                        "details": str(e),
                    },
                )
                return response.to_json()
        except Exception as e:
            response = ApiResponse(
                success=False,
                message=str(e),
                status_code=500,
                error={
                    "type": type(e).__name__,
                    "details": str(e)
                },
            )
            return response.to_json()

    @http.route("/rasha", type="http", auth="none", methods=["POST"], csrf=False)
    def Api_with_token(self, **kw):
        raw_data = request.httprequest.data
        try:
            data = json.loads(raw_data) if raw_data else {}
        except Exception as e:
            return ApiResponse(
                success=False,
                message="Invalid JSON",
                status_code=400,
                error={"type": type(e).__name__, "details": str(e)},
            ).to_json()

        login = data.get("login")
        password = data.get("password")
        db = request.db

        if login and password:
            try:
                credential = {"login": login, "password": password, "type": "password"}
                result = request.session.authenticate(db, credential)
                uid = result.get("uid")

                if uid:
                    user = request.env["res.users"].sudo().browse(uid)
                    payload = {
                        "uid": uid,
                        "user_name": user.name,
                        "db": db,
                    }
                    token = generate_token(payload)

                    return ApiResponse(
                        message=f"Hello {user.name}",
                        data={**student_profile()},
                    ).to_json(token)
                    # {
                    #     "message": f"Hello {user.name}",
                    #     "access_token": token,
                    #     "uid": uid,
                    # }

            except Exception as e:
                return ApiResponse(
                    success=False,
                    message="Authentication failed",
                    status_code=500,
                    error={"type": type(e).__name__, "details": str(e)},
                ).to_json()

        return ApiResponse(
            success=False, message="Missing login or password", status_code=400
        ).to_json()

    @http.route(
        "/api/create_student", type="http", auth="user", methods=["POST"], csrf=False
    )
    def create_student(self, **kw):
        
        auth_header = request.httprequest.headers.get("Authorization")
        if not auth_header:
            return ApiResponse(
                success=False, message="Missing Authorization header", status_code=401
            ).to_json()
        token = auth_header.split(" ")[1] if " " in auth_header else None
        is_valid, payload_or_error = verify_token(token)
        if not is_valid:
            return ApiResponse(
                success=False, message=payload_or_error, status_code=401
            ).to_json()
        try:
            data = (
                json.loads(request.httprequest.data) if request.httprequest.data else {}
            )
        except Exception as e:
            return ApiResponse(
                success=False,
                message="Invalid JSON",
                status_code=400,
                error={"type": type(e).__name__, "details": str(e)},
            ).to_json()
        name = data.get("name")
        email = data.get("email")
        school_id = data.get("school_id")

        if not name or not email or not school_id:
            return ApiResponse(
                success=False,
                message="Missing required fields: name, email, school_id",
                status_code=400,
            ).to_json()

        student = request.env["school.student"].sudo().create(
            {"name": name, "email": email, "school_id": int(school_id)}
        )
        return ApiResponse(
            success=True,
            message="Student created successfully",
            data={
                "id": student.id,
                "name": student.name,
                "email": student.email
            }
        ).to_json()
    

    @http.route("/school_student/school_student/objects", auth="public")
    def list(self, **kw):
        return http.request.render(
            "school_student.listing",
            {
                "root": "/school_student/school_student",
                "objects": http.request.env["school.student"].search([]),
            },
        )

    #         return request.make_json_response({
    #     'status': 'success',
    #     'message': 'Data received'
    # })
    # return request.not_found()

    @http.route("/download/report", type="http", auth="user")
    def download_report(self):
        content = "Student Name, Grade\nAhmed, A\nSara, B"

        # إعداد الترويسات لإخبار المتصفح بأن هذا ملف للتحميل
        headers = [
            ("Content-Type", "text/csv"),
            ("Content-Disposition", 'attachment; filename="students.csv"'),
        ]

        return request.make_response(content, headers=headers)

    @http.route(
        '/school_student/school_student/objects/<model("school.student"):obj>',
        auth="public",
        methods=["GET"],
    )
    def object(self, obj, **kw):
        return http.request.render("school_student.object", {"object": obj})

    @http.route("/go_home", type="http", auth="public")
    def go_home(self):
        # إعادة توجيه إلى رابط آخر (كود 302)
        return request.redirect("/school_student/school_student")

    @http.route("/check/header", type="http", auth="none")
    def check_header(self):
        # الوصول للـ Headers القادمة من المتصفح
        user_agent = request.httprequest.headers.get("User-Agent")
        token = request.httprequest.headers.get("Authorization")

        return f"أنت تتصفح من: ----{token}"

    # @http.route('/api/check_token', type='http', auth='none', cors='*')
    # def check_token(self):
    #     # جلب الـ Header الذي يحتوي على التوكن
    #     auth_header = request.httprequest.headers.get('Authorization')

    #     if auth_header:
    #         # طباعة التوكن في الـ Log الخاص بأودو
    #         _logger.info("---------- Token Received ----------")
    #         _logger.info(auth_header)
    #         _logger.info("------------------------------------")

    #         return f"تم استلام التوكن: {auth_header}"
    #     else:
    #         return "لا يوجد توكن في الـ Headers"

    @http.route("/check_browser_token", type="http", auth="user")
    def check_browser_token(self):
        # في المتصفح، التوكن هو معرف الجلسة
        session_id = request.session.sid

        # أو يمكنك جلبه من الكوكيز مباشرة عبر الهيدرز
        all_cookies = request.httprequest.cookies

        return f"""
            <h3>بيانات الجلسة في المتصفح:</h3>
            <p><b>Session ID (sid):</b> {session_id}</p>
            <p><b>كل الكوكيز:</b> {all_cookies}</p>
        """

    @http.route("/check_my_header", type="http", auth="none", cors="*")
    def check_header(self):
        headers = request.httprequest.headers
        token = headers.get("Authorization") or headers.get("authorization")

        user_agent = headers.get("User-Agent", "Unknown Browser")

        if token:
            return f"أنت تتصفح من: {user_agent} <br/> Bearer Token is: {token}"
        else:
            all_headers = "<br/>".join([f"{k}: {v}" for k, v in headers.items()])
            return f"لم يتم العثور على التوكن. الهيدرز المستلمة هي: <br/> {all_headers}"


class ControllerName(SchoolStudent):

    @http.route()
    def index(self, **kw):
        print(f"Sucess----------------------------{self}")
        return super(ControllerName, self).index(**kw)
