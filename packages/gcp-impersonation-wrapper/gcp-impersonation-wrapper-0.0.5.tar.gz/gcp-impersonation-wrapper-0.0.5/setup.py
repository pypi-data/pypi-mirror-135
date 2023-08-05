import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gcp-impersonation-wrapper",
    version="0.0.5",
    packages=setuptools.find_packages(),
    long_description_content_type="text/markdown",
    long_description=long_description,
    python_requires=">=3.7",
    install_requires=[
        "requests",
        "httplib2",
        "google-api-core",
        "google-api-python-client",
        "google-auth",
        "google-cloud-core",
        "google-resumable-media",
        "googleapis-common-protos",
        "google-auth-oauthlib",
        "oauth2client",
    ],
    url="https://gitlab.com/dqna/dv-data-generator",
)
