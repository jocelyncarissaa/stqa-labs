Feature: Pet CRUD & Search
  As a pet shop application user
  I want to be able to manage the pets in my pet shop using the application
  So that I can keep track of the pets in my pet shop

  Background:
    Given I am in the home page
    And the pet list is empty

  Scenario: Validate pet creation
    When I create a pet with name "Buddy", category "dog", gender "MALE", birthday "2024-01-01"
    Then the pet list should show "Buddy" with the correct details: "dog", "MALE", "2024-01-01"

  Scenario: Validate pet update
    When I create a pet with name "Buddy", category "dog", gender "MALE", birthday "2024-01-01"
    And I update pet ID "1" with only a new name "Buddy Jr."
    Then the pet list should show "Buddy Jr." with the correct details: "dog", "MALE", "2024-01-01"

  Scenario: Validate pet delete
    When I create a pet with name "Buddy", category "dog", gender "MALE", birthday "2024-01-01"
    And I delete pet ID "1"
    Then the pet list should not show "Buddy"

  Scenario: Search by name
    When I create a pet with name "Buddy", category "dog", gender "MALE", birthday "2024-01-01"
    And I create a pet with name "Fido", category "dog", gender "MALE", birthday "2025-06-01"
    When I search for the name "Fido"
    Then the pet list should show "Fido"
    And the pet list should not show "Buddy"

  Scenario: Search by category is case-insensitive
    When I create a pet with name "Buddy", category "dog", gender "MALE", birthday "2024-01-01"
    And I create a pet with name "Neko", category "cat", gender "FEMALE", birthday "2025-03-15"
    When I search for the category "Cat"
    Then the pet list should show "Neko"
    And the pet list should not show "Buddy"
