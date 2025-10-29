@echo off
echo 🧪 Testing Evolusis Agent - Complete Requirements Validation
echo ============================================================
echo.

set BASE_URL=http://localhost:8000

echo 1. TESTING FASTAPI BACKEND & SINGLE ENDPOINT
echo --------------------------------------------
curl -X GET "%BASE_URL%/"
echo.
curl -X GET "%BASE_URL%/health"
echo.
curl -X POST "%BASE_URL%/ask" -H "Content-Type: application/json" -d "{\"query\": \"test connection\"}"
echo.

echo.
echo 2. TESTING LLM API INTEGRATION
echo ------------------------------
curl -X POST "%BASE_URL%/ask" -H "Content-Type: application/json" -d "{\"query\": \"Explain the concept of machine learning\"}"
echo.
curl -X POST "%BASE_URL%/ask" -H "Content-Type: application/json" -d "{\"query\": \"Write a short poem about technology\"}"
echo.

echo.
echo 3. TESTING EXTERNAL API INTEGRATION
echo -----------------------------------
curl -X POST "%BASE_URL%/ask" -H "Content-Type: application/json" -d "{\"query\": \"What is the weather in London?\"}"
echo.
curl -X POST "%BASE_URL%/ask" -H "Content-Type: application/json" -d "{\"query\": \"Who invented the telephone?\"}"
echo.
curl -X POST "%BASE_URL%/ask" -H "Content-Type: application/json" -d "{\"query\": \"Latest news about artificial intelligence\"}"
echo.

echo.
echo 4. TESTING INTELLIGENT DECISION-MAKING
echo --------------------------------------
curl -X POST "%BASE_URL%/ask" -H "Content-Type: application/json" -d "{\"query\": \"What are the benefits of renewable energy?\"}"
echo.
curl -X POST "%BASE_URL%/ask" -H "Content-Type: application/json" -d "{\"query\": \"Should I take an umbrella in Paris today?\"}"
echo.
curl -X POST "%BASE_URL%/ask" -H "Content-Type: application/json" -d "{\"query\": \"What is the capital of Japan?\"}"
echo.

echo.
echo 5. TESTING RESPONSE FORMAT
echo --------------------------
curl -X POST "%BASE_URL%/ask" -H "Content-Type: application/json" -d "{\"query\": \"weather in Tokyo\"}"
echo.

echo.
echo 6. TESTING MEMORY SYSTEM (BONUS FEATURE)
echo ----------------------------------------
curl -X GET "%BASE_URL%/memory"
echo.
curl -X DELETE "%BASE_URL%/memory"
echo.

echo.
echo 7. TESTING ERROR HANDLING
echo -------------------------
curl -X POST "%BASE_URL%/ask" -H "Content-Type: application/json" -d "{\"query\": \"\"}"
echo.
curl -X POST "%BASE_URL%/ask" -H "Content-Type: application/json" -d "{\"query\": \"weather in InvalidCityName123\"}"
echo.

echo.
echo ============================================================
echo ✅ ALL TESTS COMPLETED!
echo.
pause