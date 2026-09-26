from src.test.graph.graph import app


if __name__ == "__main__":
    print(app.invoke(input={"question": "agent memory?"}))