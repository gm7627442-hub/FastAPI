from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import models
from storage import accounts
import auth

app = FastAPI(title="Auth API")

@app.post("/register", response_model=models.AccountResponse, status_code=status.HTTP_201_CREATED)
def register(account: models.Account):
    for acc in accounts:
        if acc["username"] == account.username:
            raise HTTPException(status_code=400, detail="Username already registered")
    
    new_account = account.model_dump()
    accounts.append(new_account)
    return new_account

@app.post("/login", response_model=models.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    target_account = None
    for acc in accounts:
        if acc["username"] == form_data.username:
            target_account = acc
            break
            
    if not target_account or target_account["password"] != form_data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        
    access_token = auth.create_access_token(data={"sub": target_account["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=models.AccountResponse)
def get_me(current_account: dict = Depends(auth.get_current_account)):
    return current_account

@app.get("/admin/stats")
def get_admin_stats(current_account: dict = Depends(auth.get_current_account)):
    auth.check_admin_role(current_account)
    return {"total_accounts": len(accounts), "status": "all systems operational"}
