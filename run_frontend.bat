@echo off
echo Setting up and starting React frontend...

cd frontend

if not exist node_modules (
    echo Installing npm dependencies...
    npm install
)

echo Starting development server...
npm run dev

pause