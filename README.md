# This is Flaconi Interview Assignment
- Please create a public repo on Git

- Create automation tests for the following scenarios:

1. add to cart a random product from Parfum category
2. on the Cart page to verify if we are displaying the correct price
3. verify the main navigation menu links

URL: https://www.flaconi.de/

# Technology Used: 
Python and Selenium

# Solution:
Approach - I have designed a small framework(POM) for automating above scenarios.

Below is the folder structure followed:

# Folder_Structure
base:
	selenium_driver.py -- This file holds all selenium related functions that are used in the test scripts.

pages:
	All above use cases are placed in this folder
	1. PerfumeSelection.py - Navigate to Perfume Category and select required Perfume
	2. PerfumeDetailBeforeFinalSelection.py - After perfume is selected, pop-up comes to verify perfume selected. We get Perfume details to make sure same is added to cart.
	3. GetDetailsBeforeAddingToCart.py - After confirming to the selection, we need to confirm if following needs to be added to cart. We get Perfume details to make sure same is added to cart.
	4. PerfumeDetailFromCart.py - We move to cart page, where we validate selected perfume is preperly displayed on the cart.
tests:
	This folder holds Test Cases(executed for above scenarios) and initiallization for selenium webdriver.
	1. conftest.py - Holds setup and teardown for selenium webdriver. Also holds details for browser exection.
	2. TestCases.py - This holds pytest for tests to be executed.
utility:
	This folder holds logging mechanism for complete test exection.

# Logging:
Automation_Test_Log.log is generated with each execution.

# Execution Process
cd //path to Flaconi_Assessment
set PYTHONPATH=%PYTHONPATH%;%CD%
echo %PYTHONPATH%

py.test -v -s \tests\Test_Cases.py --html=Report.html


