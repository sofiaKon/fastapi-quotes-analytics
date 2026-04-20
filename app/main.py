from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.api.routes import router

from app.ui.gradio_app import create_interface
import gradio as gr

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quotes Analytics System")

app.include_router(router)

gradio_app = create_interface()
app = gr.mount_gradio_app(app, gradio_app, path="/ui")


@app.get("/")
def read_root():
    return {"message": "Quotes Analytics System is running"}
