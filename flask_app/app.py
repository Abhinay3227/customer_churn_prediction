from flask import Flask, render_template, request, redirect, session
import pickle
import pandas as pd
import mysql.connector
import os


print("RUNNING FROM:", os.getcwd())

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)

print("APP FILE:", __file__)
print("TEMPLATE FOLDER:", app.template_folder)
print("FILES IN TEMPLATE:", os.listdir(app.template_folder))

app.secret_key = "secret123"

# LOAD MODEL
model = pickle.load(open("model/churn_model.pkl", "rb"))
scaler = pickle.load(open("model/churn_scaler.pkl", "rb"))
columns = pickle.load(open("model/model_columns.pkl", "rb"))

# DB CONNECTION
def get_db():
    return mysql.connector.connect(
        host="nozomi.proxy.rlwy.net",
        user="root",
        password="VYFqFPzERsQqShZSVivbYkamqCqSpRaK",
        database="railway",
        port=24503
    )

# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            session["user"] = "admin"
            return redirect("/home")   # 🔥 FIXED
    return render_template("login.html")

@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/")
    return render_template("home.html")

# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    conn = get_db()

    # LOAD DATA
    df = pd.read_sql("SELECT * FROM predictions", conn)

    total = len(df)
    churn = len(df[df["prediction"] == 1])
    stay = len(df[df["prediction"] == 0])

    # TREND GRAPH
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DATE(created_at), COUNT(*)
        FROM predictions
        WHERE prediction = 1
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at)
    """)

    trend_data = cursor.fetchall()

    trend_dates = [str(x[0]) for x in trend_data]
    trend_values = [x[1] for x in trend_data]

    return render_template(
                            "dashboard.html",
                            total=total,
                            churn=churn,
                            stay=stay,
                            trend_dates=trend_dates,
                            trend_values=trend_values
                        )
# PREDICT
@app.route("/predict", methods=["GET", "POST"])
def predict():

    if "user" not in session:
        return redirect("/")

    result = None
    prob = None
    reasons = []
    insights = []
    suggestions = []

    if request.method == "POST":

        tenure = int(request.form["tenure"])
        monthly = float(request.form["monthly"])
        total = float(request.form["total"])

        senior_option = request.form["senior"]
        partner = request.form["partner"]
        dependents = request.form["dependents"]

        phone = request.form["phone"]
        internet = request.form["internet"]
        contract = request.form["contract"]
        paperless = request.form["paperless"]

        senior = 1 if senior_option == "Yes" else 0

        # EXACT SAME SAMPLE AS STREAMLIT
        sample = pd.DataFrame({
            "SeniorCitizen": [senior],
            "tenure": [tenure],
            "MonthlyCharges": [monthly],
            "TotalCharges": [total],
            "Partner": [partner],
            "Dependents": [dependents],
            "PhoneService": [phone],
            "InternetService": [internet],
            "Contract": [contract],
            "PaperlessBilling": [paperless]
        })

        # EXACT SAME PREPROCESSING
        sample = pd.get_dummies(sample)
        sample = sample.reindex(columns=columns, fill_value=0)

        sample_scaled = scaler.transform(sample)

        # EXACT SAME PREDICTION
        pred = model.predict(sample_scaled)[0]
        prob = model.predict_proba(sample_scaled)[0][1]

        # DATABASE SAVE
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO predictions
            (tenure, monthly, total, contract, prediction, probability)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            tenure,
            monthly,
            total,
            contract,
            int(pred),
            float(prob)
        ))

        conn.commit()

        # SAME RESULT LOGIC
        if pred == 1:
            result = f"⚠ Customer Likely to Churn ({prob*100:.2f}%)"
        else:
            result = f"✅ Customer Will Stay ({(1-prob)*100:.2f}%)"

        # =========================
        # SAME REASONS
        # =========================
        if pred == 1:

            if tenure < 12:
                reasons.append("Customer is new (low tenure)")

            if monthly > 80:
                reasons.append("High monthly charges")

            if "month" in contract.lower():
                reasons.append("No long-term contract")

            if "fiber" in internet.lower():
                reasons.append("Expensive internet service")

            # =========================
            # SAME INSIGHTS
            # =========================

            if monthly > 80:
                insights.append("🔺 High charges increase churn risk")
            else:
                insights.append("🔻 Affordable charges reduce churn risk")

            if tenure < 12:
                insights.append("🔺 Short tenure increases churn")
            else:
                insights.append("🔻 Long-term customers are stable")

            if "month" in contract.lower():
                insights.append("🔺 Month-to-month contract is risky")
            else:
                insights.append("🔻 Long-term contract reduces churn")

            if "fiber" in internet.lower():
                insights.append("🔺 Fiber users tend to churn more")

            # =========================
            # SAME SUGGESTIONS
            # =========================

            if monthly > 80:
                suggestions.append("Offer discount or cheaper plan")

            if "month" in contract.lower():
                suggestions.append("Encourage long-term contract")

            if tenure < 12:
                suggestions.append("Provide onboarding support")

    return render_template(
    "predict.html",

    result=result,
    prob=prob,
    reasons=reasons,
    insights=insights,
    suggestions=suggestions,

    tenure=tenure if request.method == "POST" else "",
    monthly=monthly if request.method == "POST" else "",
    total=total if request.method == "POST" else "",

    senior=senior_option if request.method == "POST" else "",
    partner=partner if request.method == "POST" else "",
    dependents=dependents if request.method == "POST" else "",

    phone=phone if request.method == "POST" else "",
    internet=internet if request.method == "POST" else "",
    contract=contract if request.method == "POST" else "",
    paperless=paperless if request.method == "POST" else ""
)
    
# DATABASE
@app.route("/database")
def database():

    if "user" not in session:
        return redirect("/")

    conn = get_db()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM predictions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    return render_template(
        "database.html",
        rows=rows
    )

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        file = request.files["file"]

        if file:
            df = pd.read_csv(file)

            conn = get_db()
            cursor = conn.cursor()

            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO predictions (tenure, monthly, total, contract, prediction, probability)
                    VALUES (%s,%s,%s,%s,%s,%s)
                """, (
                    row["tenure"],
                    row["MonthlyCharges"],
                    row["TotalCharges"],
                    row["Contract"],
                    int(row["prediction"]),
                    float(row["probability"])
                ))

            conn.commit()

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)