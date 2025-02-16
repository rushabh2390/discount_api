### Fastapi Discount Api
---
This is ecommerce module where customer can add items in order and then check out and applied coupon if valid.

### How to run this.
---   
1. Set up .env file with following keys.Set value as per your requirements
````
SECRET_KEY=xxxx #this is for encryption of token
````
2. Install dependenceny   
````
pip install -r requirements.txt
````
3. Run the below command to start fastapi
````
uvicorn main:app --reload
````
4. You can see api swagger here [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)