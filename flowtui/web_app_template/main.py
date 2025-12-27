import uvicorn
import importlib
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# --- App Setup ---
# Use pathlib to ensure paths are relative to this script's location
BASE_DIR = Path(__file__).resolve().parent
app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "views")

# --- The "Flow" System Runner ---
# This is the universal endpoint that makes the whole system work.
@app.post("/___flow___")
async def handle_flow(request: Request):
    payload = await request.json()
    flow_name = payload.get("flow") # e.g., "products"
    method_name = payload.get("method") # e.g., "add_item"
    params = payload.get("params", {})

    try:
        # 1. Dynamically import the flow module
        # Convention: flow name "products" maps to "flows.products" module
        module = importlib.import_module(f"flows.{flow_name}")
        
        # Convention: Class name is the capitalized version of the flow name, e.g., "Products"
        FlowClass = getattr(module, flow_name.capitalize())
        flow_instance = FlowClass()

        # 2. Call the specified method
        # Convention: Method name from JS maps directly to a Python method.
        method_to_call = getattr(flow_instance, method_name)
        result_data = method_to_call(params)

        # 3. Render the corresponding template partial
        # Convention: For a method like "add_item", we render a partial named "_item.html"
        # This assumes methods that add/update single items render the item partial.
        template_name = f"{flow_name}/_item.html"
        
        # Add the request object to the context for Jinja2
        template_context = {"request": request, **result_data}
        return templates.TemplateResponse(template_name, template_context)

    except (ModuleNotFoundError, AttributeError) as e:
        return HTMLResponse(content=f"Error: Could not handle flow. {e}", status_code=500)
    except Exception as e:
        return HTMLResponse(content=f"An unexpected error occurred: {e}", status_code=500)


# --- Initial Page Load ---
# This just renders the main page for the first time.
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # This is how you would call a flow from the server-side for the initial render
    from flows.products import Products
    products_flow = Products()
    initial_data = products_flow.get_all()
    return templates.TemplateResponse("products/index.html", {"request": request, **initial_data})

if __name__ == "__main__":
    # Note: Running this script directly will fail due to relative imports.
    # Run with: uvicorn web_app_template.main:app --reload
    print("To run this app, use the command:")
    print("uvicorn web_app_template.main:app --reload")

