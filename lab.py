"""Local analyst workbench for selecting and exporting verified survey evidence."""
import json
from io import BytesIO
from pathlib import Path
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel
from pptx import Presentation
from pptx.util import Inches

ROOT = Path(__file__).resolve().parent


class Decision(BaseModel):
    topic: str
    include: bool


def create_app(database, evidence):
    app = FastAPI(title="Employee Sentiment Analysis | Voice Lab")
    topics = {row["topic"]: row for row in evidence["topics"]}
    with sqlite3.connect(database) as con:
        con.execute("CREATE TABLE IF NOT EXISTS selection(topic TEXT PRIMARY KEY, chosen INTEGER NOT NULL)")

    @app.get("/", response_class=HTMLResponse)
    def view():
        return (ROOT/"index.html").read_text()

    @app.get("/topics")
    def rows():
        with sqlite3.connect(database) as con: choices = dict(con.execute("SELECT topic,chosen FROM selection"))
        return [{**row,"included":bool(choices.get(name,0))} for name,row in topics.items()]

    @app.post("/review")
    def review(d: Decision):
        if d.topic not in topics: raise HTTPException(400,"Unknown topic.")
        with sqlite3.connect(database) as con:
            con.execute("INSERT INTO selection VALUES (?,?) ON CONFLICT(topic) DO UPDATE SET chosen=excluded.chosen",(d.topic,int(d.include)))
        return {"included": d.include}

    @app.get("/brief.pptx")
    def brief():
        selected = [row for row in rows() if row["included"]]
        if not selected: raise HTTPException(409,"Approve at least one topic first.")
        deck = Presentation()
        deck.core_properties.author = deck.core_properties.last_modified_by = "Voice Lab demo"
        for row in selected:
            slide = deck.slides.add_slide(deck.slide_layouts[5])
            slide.shapes.title.text = row["topic"]
            box = slide.shapes.add_textbox(Inches(.8), Inches(2), Inches(8), Inches(3))
            box.text = (f"{evidence['focus']} | Employee Sentiment Analysis\n\n"
                        f"Favorable answers: {row['focus_yes']} of {row['focus_total']}\n"
                        f"Pooled peers: {row['peer_yes']} of {row['peer_total']}\n"
                        f"Difference: {row['gap_pp']:+.1f} percentage points")
        buf=BytesIO();deck.save(buf)
        return Response(buf.getvalue(),media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        headers={"Content-Disposition":'attachment; filename="reviewed-brief.pptx"'})
    return app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(create_app("review.sqlite3",json.loads((ROOT/"examples/summary.json").read_text())),host="127.0.0.1",port=8091)
