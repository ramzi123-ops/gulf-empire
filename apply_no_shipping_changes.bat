@echo off
echo ========================================
echo Applying No Shipping Service Changes
echo ========================================
echo.

echo Step 1: Running database migration...
python manage.py migrate
echo.

echo Step 2: Checking migration status...
python manage.py showmigrations orders
echo.

echo ========================================
echo Done! Changes Applied Successfully
echo ========================================
echo.
echo Next Steps:
echo 1. Test checkout flow (no address required)
echo 2. Verify orders create without address
echo 3. Continue with Stripe setup
echo.
echo See NO_SHIPPING_CHANGES.md for details
echo ========================================
pause
