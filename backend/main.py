import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.analyticsRoutes import router as analytics_router
from routers.deliveryAgentRoutes import router as delivery_agent_router
from routers.demoRoutes import router as demo_router
from routers.insightRoutes import router as insight_router
from routers.memoryRoutes import router as memory_router
from routers.expansionRoutes import router as expansion_router
from routers.profileRoutes import router as profile_router
from routers.authRoutes import router as auth_router
from domains.distributor.routes import router as distributor_router
from domains.restaurant.routes import router as restaurant_router
from domains.raw_material.routes import router as raw_material_router
from domains.retail.routes import router as retail_router
from domains.service_provider.routes import router as service_provider_router
from routers.recommendationRoutes import router as recommendation_router
from routers.shipmentRoutes import router as shipment_router

load_dotenv()

app = FastAPI(title='LOGIMIND', version='2.0.0')

frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, 'http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(shipment_router, prefix='/api')
app.include_router(delivery_agent_router, prefix='/api')
app.include_router(demo_router, prefix='/api')
app.include_router(analytics_router, prefix='/api')
app.include_router(insight_router, prefix='/api')
app.include_router(memory_router, prefix='/api')
app.include_router(recommendation_router, prefix='/api')
app.include_router(profile_router, prefix='/api')
app.include_router(expansion_router, prefix='/api')
app.include_router(auth_router, prefix='/api')
app.include_router(distributor_router, prefix='/api')
app.include_router(restaurant_router, prefix='/api')
app.include_router(raw_material_router, prefix='/api')
app.include_router(retail_router, prefix='/api')
app.include_router(service_provider_router, prefix='/api')


@app.get('/health')
def health_check() -> dict:
    return {'status': 'ok', 'app': 'LOGIMIND'}


# if __name__ == '__main__':
#     import uvicorn

#     uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
