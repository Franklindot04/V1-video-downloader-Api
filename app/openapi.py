def configure_openapi(app):
    original_openapi = app.openapi

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = original_openapi()

        openapi_schema["info"]["contact"] = {
            "name": "V1 Video Downloader API",
            "url": (
                "https://github.com/Franklindot04/"
                "V1-video-downloader-Api"
            ),
        }

        openapi_schema["info"]["license"] = {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT",
        }

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi