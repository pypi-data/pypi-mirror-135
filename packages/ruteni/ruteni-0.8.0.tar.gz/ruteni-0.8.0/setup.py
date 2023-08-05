from pathlib import Path

import setuptools

# with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="ruteni",
    version="0.8.0",
    author="Johnny Accot",
    description="Thin layer over Starlette",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    py_modules=["ruteni"],
    package_data={
        "ruteni": [
            str(path).replace("ruteni/dist", "dist")
            for path in Path("ruteni/dist").glob("**/*")
        ]
        + [
            str(path).replace("ruteni/", "")
            for path in Path("ruteni").glob("**/resources/**/*")
        ]
        + [
            str(path).replace("ruteni/", "")
            for path in Path("ruteni").glob("**/templates/**/*")
        ]
    },
    entry_points={
        "ruteni.service.v1": [
            "auth-api = ruteni.apis.auth.session:api_node",
            "jauthn-api = ruteni.apis.auth.token:api_node",
            "database = ruteni.services.database:database",
            "health-check = ruteni.services.health_check:health_check",
            "keys = ruteni.services.keys:key_service",
            "logging-api = ruteni.apis.logging:api_node",
            "nng = ruteni.services.nng:nng",
            "presence = ruteni.services.presence:presence",
            "register = ruteni.apps.registration:app_node",
            "scheduler = ruteni.services.scheduler:scheduler",
            "security-api = ruteni.apis.security:api_node",
            "smtpd = ruteni.services.smtpd:smtpd",
            "sshd = ruteni.services.sshd:sshd",
            "store-api = ruteni.apps.store:api_node",
            "store-app = ruteni.apps.store:app_node",
            "user-api = ruteni.apis.users:api_node",
        ],
        "ruteni.endpoint.http.v1": [],
        "ruteni.endpoint.websocket.v1": [
            "socketio = ruteni.plugins.socketio:app",
        ],
        "ruteni.node.http.v1": [
            "auth-api = ruteni.apis.auth.session:api_node",
            "jauthn-api = ruteni.apis.auth.token:api_node",
            "register = ruteni.apps.registration:app_node",
            "robots = ruteni.plugins.site:robots_node",
            "favicon = ruteni.plugins.site:favicon_node",
            "static = ruteni.plugins.static:node",
            "store-app = ruteni.apps.store:app_node",
        ],
        "ruteni.node.websocket.v1": [],
    },
    install_requires=[
        "aiodns",
        "aioredis",
        "aiosmtplib",
        "aiosmtpd",
        "aiosqlite",
        "anyio",
        "anytree",
        "apscheduler",
        "argon2_cffi",
        "asgiref",
        "asyncssh",
        "authlib",
        "babel",
        "boolean.py",
        "databases",
        "html5lib",
        "httpx",
        "itsdangerous",
        "jinja2",
        "jwcrypto",
        "limits",
        "marshmallow",
        "pillow",
        "pynng",
        "python-socketio",
        "pyrfc3339",
        "sqlalchemy",
        "sqlalchemy-utils",
        "starlette",
        "tabulate",
        "toposort",
        "totates",
        "transitions",
        "uvicorn",
        "webcolors",
        "websockets",
        "werkzeug",
        "zxcvbn",
    ],
    test_suite="tests.build_test_suite",
)
