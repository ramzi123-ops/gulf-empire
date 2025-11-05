"""
DEBUG WSGI - Use this temporarily to diagnose the issue
Copy this to your WSGI configuration file to see what's wrong
"""

import os
import sys

# Configuration
USERNAME = 'ramzi77'
PROJECT_NAME = 'gulf-empire'  # NOTE: hyphen not underscore!
PYTHON_VERSION = '3.13'

# Paths
project_home = f'/home/{USERNAME}/{PROJECT_NAME}'
venv_packages = f'/home/{USERNAME}/{PROJECT_NAME}/venv/lib/python{PYTHON_VERSION}/site-packages'

# Create a simple WSGI app that shows debug info
def application(environ, start_response):
    status = '200 OK'
    
    # Check if directories exist
    project_exists = os.path.exists(project_home)
    config_exists = os.path.exists(os.path.join(project_home, 'config'))
    venv_exists = os.path.exists(venv_packages)
    
    # Get directory contents
    try:
        project_contents = os.listdir(project_home) if project_exists else []
    except:
        project_contents = ['ERROR: Cannot list directory']
    
    output = f"""
<html>
<head><title>Django Debug Info</title></head>
<body style="font-family: monospace; padding: 20px;">
<h1>🔍 Django Debug Information</h1>

<h2>Python Information:</h2>
<pre>
Python Version: {sys.version}
Python Executable: {sys.executable}
</pre>

<h2>Path Configuration:</h2>
<pre>
Project Home: {project_home}
Venv Packages: {venv_packages}
</pre>

<h2>Directory Checks:</h2>
<pre>
Project exists: {project_exists} {'✅' if project_exists else '❌'}
Config folder exists: {config_exists} {'✅' if config_exists else '❌'}
Venv exists: {venv_exists} {'✅' if venv_exists else '❌'}
</pre>

<h2>Project Directory Contents:</h2>
<pre>
{chr(10).join(project_contents)}
</pre>

<h2>sys.path:</h2>
<pre>
{chr(10).join(sys.path)}
</pre>

<h2>Environment Variables:</h2>
<pre>
DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE', 'NOT SET')}
</pre>

<hr>
<p><strong>Next Steps:</strong></p>
<ul>
<li>If project doesn't exist: Check if code is uploaded to /home/{USERNAME}/{PROJECT_NAME}</li>
<li>If config folder doesn't exist: Your project structure might be wrong</li>
<li>If venv doesn't exist: Create virtualenv or adjust Python version</li>
</ul>

</body>
</html>
    """.encode('utf-8')
    
    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(output)))
    ]
    start_response(status, response_headers)
    return [output]
