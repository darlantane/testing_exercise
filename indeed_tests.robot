
*** Settings ***
Library    SeleniumLibrary
Suite Setup    Open Browser To Indeed
Suite Teardown    Close Browser
Test Setup    Go To    https://fr.indeed.com

*** Variables ***
${URL}    https://fr.indeed.com
${BROWSER}    Chrome
${SEARCH_TERM}    informatique
${LOCATION}    Paris

*** Keywords ***
Open Browser To Indeed
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Timeout    15 seconds

Accept Cookies
    Run Keyword And Ignore Error
    ...    Click Button    id=onetrust-accept-btn-handler

Launch Job Search
    Accept Cookies
    Wait Until Element Is Visible    name=q
    Input Text    name=q    ${SEARCH_TERM}
    Input Text    name=l    ${LOCATION}
    Press Keys    name=l    RETURN
    Wait Until Element Is Visible    css=div.job_seen_beacon

*** Test Cases ***
Test Homepage Load
    Wait Until Page Contains Element    tag=body

Test Page Title
    Title Should Contain    Indeed

Test Search Fields Presence
    Accept Cookies
    Element Should Be Visible    name=q
    Element Should Be Visible    name=l

Test Job Search
    Launch Job Search

Test First Result Contains Title
    Launch Job Search
    Wait Until Element Is Visible    css=h2.jobTitle

Test Click First Job
    Launch Job Search
    Click Element    css=h2.jobTitle a

Test Pagination
    Launch Job Search
    Click Element    css=a[aria-label="Suivant"]

Test Navigation Companies Page
    Accept Cookies
    Click Element    partial link=Entreprises
    Wait Until Page Contains Element    tag=body
