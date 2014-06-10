*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${CONTROL_PANEL} =  ${PLONE_URL}/plone_control_panel
${SITE_PROPERTIES} =  ${PLONE_URL}/@@site-controlpanel
${PORTAL_MODELO_SETTINGS} =  ${PLONE_URL}/@@portalmodelo-settings
${site_title_selector} =  input.textType[type="text"]
${title_selector} =  input#form-widgets-title
${kind_selector} =  select#form-widgets-kind
${address_selector} =  input#form-widgets-address
${postal_code_selector} =  input#form-widgets-postal_code
${city_selector} =  input#form-widgets-city
${state_selector} =  select#form-widgets-state
${id_selector} =  input#form-widgets-id
${telephone_selector} =  input#form-widgets-telephone
${email_selector} =  input#form-widgets-email

*** Test cases ***

Test Site Properties Synchronization
    [documentation]  Test the title of the portal can be changed from the new
    ...              configlet and is kept synchronized with the original
    ...              form.
    Enable Autologin as  Manager
    Go to  ${CONTROL_PANEL}
    Page Should Contain  Portal Modelo Settings

    # the title should be the same of the Portal
    Go to  ${PORTAL_MODELO_SETTINGS}
    Page Should Contain  Plone site

    Input Text  css=${title_selector}  Clube Atlético Juventus
    Select From List  css=${kind_selector}  outro
    Input Text  css=${address_selector}  Rua Comendador Roberto Ugolini, 20
    Input Text  css=${postal_code_selector}  03125-010
    Input Text  css=${city_selector}  Mooca
    Select From List  css=#form-widgets-state  SP
    Input Text  css=${id_selector}  62.863.444/0002-99
    Input Text  css=${telephone_selector}  +55 11 2271-2000
    Input Text  css=${email_selector}  foo@bar.com
    Click Button  Save
    Page Should Contain  Changes saved

    Go to  ${SITE_PROPERTIES}
    # the title should be the one we just set up
    Page Should Contain  Clube Atlético Juventus

    Input Text  css=${site_title_selector}  Don't Panic
    Click Button  Save
    Page Should Contain  Changes saved

    Go to  ${PORTAL_MODELO_SETTINGS}
    # the title is synchronized
    Page Should Contain  Don't Panic
