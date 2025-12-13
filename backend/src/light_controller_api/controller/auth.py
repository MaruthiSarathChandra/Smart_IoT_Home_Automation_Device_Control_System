
from flask import Blueprint, jsonify, request, render_template, redirect, make_response

# use WTForms Form class, not tkinter
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from backend.src.light_controller_api.service.jwt_service import create_jwt_token, validate_jwt_token
from backend.src.light_controller_api.service.auth_service import AuthService



auth_bp = Blueprint('auth', __name__)


#register form
class RegisterForm(Form):
    gmail_id = StringField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Enter your gmail id"}
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Enter your password"}
    )
    confirm_password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Re-Enter your password"}
    )
    submit = SubmitField('Create Account')


# login form
class LoginForm(Form):
    gmail_id = StringField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Enter your gmail id"}
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Enter your password"}
    )
    submit = SubmitField('Login')






# ---------- API FOR WEB ----------
@auth_bp.route("/register", methods=['GET', 'POST'])
def register():

    form = RegisterForm(request.form)

    #flag = "code to register to database and send back a jwttoken"
    if request.method == "POST" and form.validate():
        print("entered")

        gmail_id = form.gmail_id.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if password != confirm_password:
            return render_template("register.html", form=form, error="Passwords don't match")

        service = AuthService()

        try:
            response = service.register(gmail_id, password)
            print(response)
        except Exception as e:
            return render_template("register.html", form=form, error=str(e))

        return redirect("/api/auth/login")

    return render_template("register.html", form=form)



@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if validate_jwt_token(request):
        response = make_response(redirect("/api/home"))
        response.user = request.cookies.get('access_token')
        return response

    form = LoginForm(request.form)

    # flag
    if request.method == "POST" and form.validate():

        gmail_id = form.gmail_id.data
        password = form.password.data

        verification = AuthService().login(gmail_id, password)
        if not verification:
            return render_template("register.html", form=form, error="Invalid credentials")

        token = create_jwt_token(gmail_id)


        response = make_response(redirect("/api/home/"))
        # Set the JWT as an HttpOnly cookie
        response.set_cookie(
            'access_token',
            token,
            httponly=True,
            secure=False,  # Use secure=True in production with HTTPS
            samesite="Lax"  # Cookie expiration in seconds (e.g., 1 hour)
        )
        return response

    return render_template("login.html", form=form)






# ---------- API FOR MOBILE ----------
@auth_bp.route("/mobile/api/register", methods=["POST"])
def api_register():
    data = request.get_json()

    form = RegisterForm(data=data)
    if not form.validate():
        return jsonify({"errors": form.errors}), 400

    # flag = save to database...
    return  redirect("/mobile/api/login")


@auth_bp.route('/mobile/api/login', methods=['POST'])
def api_login():
    data = request.get_json()

    form = LoginForm(data=data)
    if not form.validate():
        return jsonify({"errors": form.errors}), 400

    #flag = verify
    return redirect("/home")

