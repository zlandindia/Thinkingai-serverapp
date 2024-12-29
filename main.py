from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import razorpay
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

RAZORPAY_KEY_ID = "rzp_live_EAvzuQ7vxdvCpX"
RAZORPAY_KEY_SECRET = "c8mI2L6iRzRjAk7ssZ7ZmQde"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Define request structure for subscription creation
class SubscriptionRequest(BaseModel):
    plan_id: str  # Razorpay Plan ID
    customer_notify: int = 1  # Notify customer (1 = Yes, 0 = No)
    total_count: int = 120  # Number of billing cycles (e.g., 12 for 1 year)
    notes: dict = {}  # Optional metadata

# Endpoint to create Razorpay subscription
@app.post("/create-subscription")
def create_subscription(request: SubscriptionRequest):
    print("API Called")
    try:
        # Create subscription on Razorpay
        subscription = razorpay_client.subscription.create({
            "plan_id": request.plan_id,
            "customer_notify": request.customer_notify,
            "total_count": request.total_count,
            "notes": request.notes,
        })
        return subscription
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))