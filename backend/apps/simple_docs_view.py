"""
Simple API documentation view as fallback for Swagger
"""
from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def simple_api_docs(request):
    """Returns a simple HTML page with API documentation"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cohort API Documentation</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
            h1 { color: #333; }
            h2 { color: #666; border-bottom: 2px solid #eee; padding-bottom: 10px; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { display: inline-block; padding: 5px 10px; border-radius: 3px; font-weight: bold; }
            .get { background: #61affe; color: white; }
            .post { background: #49cc90; color: white; }
            .put { background: #fca130; color: white; }
            .delete { background: #f93e3e; color: white; }
            code { background: #eee; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🚀 Cohort Web API Documentation</h1>
        <p><strong>Base URL:</strong> <code>https://cohort-backend-api.onrender.com/api</code></p>
        <p><strong>Frontend:</strong> <a href="https://cohort.pages.dev">https://cohort.pages.dev</a></p>
        
        <h2>Authentication</h2>
        <div class="endpoint">
            <span class="method post">POST</span> <code>/api/auth/token/</code>
            <p>Obtain JWT token for authentication</p>
            <strong>Request Body:</strong>
            <pre>{"email": "user@example.com", "password": "password"}</pre>
            <strong>Response:</strong>
            <pre>{"access": "token...", "refresh": "token..."}</pre>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span> <code>/api/auth/token/refresh/</code>
            <p>Refresh JWT access token</p>
        </div>
        
        <h2>Health & Status</h2>
        <div class="endpoint">
            <span class="method get">GET</span> <code>/api/health/</code>
            <p>Check API health status</p>
        </div>
        
        <h2>User Profile</h2>
        <div class="endpoint">
            <span class="method get">GET</span> <code>/api/profiles/</code>
            <p>Get user profile information</p>
            <p><strong>Auth Required:</strong> Yes (Bearer token)</p>
        </div>
        
        <h2>Dashboard</h2>
        <div class="endpoint">
            <span class="method get">GET</span> <code>/api/dashboard/stats/</code>
            <p>Get dashboard statistics</p>
        </div>
        
        <h2>Applications</h2>
        <ul>
            <li><code>/api/clt/</code> - CLT module</li>
            <li><code>/api/cfc/</code> - CFC module</li>
            <li><code>/api/iipc/</code> - IIPC module</li>
            <li><code>/api/scd/</code> - SCD module</li>
            <li><code>/api/hackathons/</code> - Hackathons</li>
            <li><code>/api/gamification/</code> - Gamification system</li>
        </ul>
        
        <h2>Admin Endpoints</h2>
        <div class="endpoint">
            <span class="method get">GET</span> <code>/api/admin/</code>
            <p>Admin panel APIs (requires admin role)</p>
        </div>
        
        <h2>Mentor Endpoints</h2>
        <div class="endpoint">
            <span class="method get">GET</span> <code>/api/mentor/</code>
            <p>Mentor dashboard APIs (requires mentor role)</p>
        </div>
        
        <hr>
        <p><small>For full interactive documentation, visit <a href="/api/docs/">/api/docs/</a></small></p>
    </body>
    </html>
    """
    return HttpResponse(html, content_type="text/html")
