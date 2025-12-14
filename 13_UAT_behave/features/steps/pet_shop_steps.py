import requests
from behave import given, when, then
from selenium.webdriver.common.by import By
import time

@given('I am in the home page')
def step_impl(context):
    context.driver.get(context.base_url)

@given('the pet list is empty')
def step_impl(context):
    requests.post(f"{context.base_url}/pets/reset")

def fill_pet_form(context, name="", category="", gender=None, birthday=None, available=True):
    if name:
        context.driver.find_element(By.ID, "pet_name").send_keys(name)
    if category:
        context.driver.find_element(By.ID, "pet_category").send_keys(category)
    if gender:
        context.driver.find_element(By.ID, "pet_gender").send_keys(gender)
    if birthday:
        date_element = context.driver.find_element(By.ID, "pet_birthday")
        context.driver.execute_script(
            "arguments[0].value = arguments[1];", 
            date_element, 
            birthday
        )
    checked = context.driver.find_element(By.ID, "pet_available").is_selected()
    if available != checked:
        context.driver.find_element(By.ID, "pet_available").click()

def create_pet(context, name, category, gender=None, birthday=None, available=True):
    fill_pet_form(context, name, category, gender, birthday, available)
    context.driver.find_element(By.ID, "create-btn").click()
    time.sleep(0.5)

@when('I create a pet with name "{pet_name}", category "{pet_category}", gender "{pet_gender}", birthday "{pet_birthday}"')
def step_impl(context, pet_name, pet_category, pet_gender, pet_birthday):
    create_pet(context, pet_name, pet_category, pet_gender, pet_birthday, available=True)

@then('the pet list should show "{pet_name}" with the correct details: "{pet_category}", "{pet_gender}", "{pet_birthday}"')
def step_impl(context, pet_name, pet_category, pet_gender, pet_birthday):
    results_text = context.driver.find_element(By.ID, "search_results").text
    print(results_text)
    print(pet_name, pet_category, pet_gender, pet_birthday)
    assert pet_name in results_text, "Name problem"
    assert pet_category in results_text, "Category problem"
    assert pet_gender in results_text, "Gender problem"
    assert pet_birthday in results_text, "Birthday problem"

@when('I update pet ID "{pet_id}" with only a new name "{pet_name}"')
def step_impl(context, pet_id, pet_name):
    context.driver.find_element(By.ID, "pet_id").send_keys(pet_id)
    context.driver.find_element(By.ID, "pet_name").send_keys(pet_name)
    context.driver.find_element(By.ID, "update-btn").click()
    time.sleep(0.5)

@when('I delete pet ID "{pet_id}"')
def step_impl(context, pet_id):
    context.driver.find_element(By.ID, "pet_id").send_keys(pet_id)
    context.driver.find_element(By.ID, "delete-btn").click()
    time.sleep(0.5)

@then('the pet list should not show "{pet_name}"')
def step_impl(context, pet_name):
    results_text = context.driver.find_element(By.ID, "search_results").text
    assert pet_name not in results_text

@when('I search for the name "{pet_name}"')
def step_impl(context, pet_name):
    context.driver.find_element(By.ID, "pet_name").send_keys(pet_name)
    context.driver.find_element(By.ID, "search-btn").click()
    time.sleep(0.5)

@then('the pet list should show "{pet_name}"')
def step_impl(context, pet_name):
    results_text = context.driver.find_element(By.ID, "search_results").text
    assert pet_name in results_text

@when('I search for the category "{pet_category}"')
def step_impl(context, pet_category):
    context.driver.find_element(By.ID, "pet_category").send_keys(pet_category)
    context.driver.find_element(By.ID, "search-btn").click()
    time.sleep(0.5)