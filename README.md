# Django SaaS Project

Build the foundations for a Software as a Service business by leveraging Django, Tailwind, htmx, Neon Postgres, Redis, and more.

The goal of this project is to learn how to create a reusable foundation for building SaaS products for your business or startup.

## References

- Deploy DJango on [Railway](https://railway.app/?referralCode=fgkUis) with this [Dockerfile and guide](https://www.codingforentrepreneurs.com/blog/deploy-django-on-railway-with-this-dockerfile)
- Use a serverless postgress with [Neon](https://neon.tech/) 


## Getting Started
### Clone
```bash
git clone https://github.com/codeabuu/saas
```
### Create a Virtual Environment
*mac0S/Linux*
```bash
python3 --version # should be 3.11 or higher
python3 -m venv venv
source venv/bin/activate
```

*Windows*
```bash
c:\Python312\python.exe -m venv venv
.\venv\Scripts\activate
```
### Install Requirements
```bash
# with venv activated
pip install pip --upgrade && pip install -r requirements.txt
```
### Sample dotenev to dotnev
```bash
cp .env.sample .env
cat .env
```

