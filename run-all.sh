#!/bin/bash

# Start backend
echo "Starting backend..."
cd backend
source venv/bin/activate
python run.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID