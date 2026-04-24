from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.api.routes.quotes import router as quotes_router
from app.api.routes.analys import router as analytics_router
from app.ui.gradio_app import create_interface
import gradio as gr

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quotes Analytics System")

app.include_router(quotes_router)
app.include_router(analytics_router)

gradio_app = create_interface()
app = gr.mount_gradio_app(app, gradio_app, path="/ui")


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Quotes Analytics System is running"}
