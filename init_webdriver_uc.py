import undetected_chromedriver as uc

def init_webdriver_ec(headless=False, pos="maximizada",usar_devtools=False, extensiones=None):

    options = uc.ChromeOptions()

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-features=Translate")
    options.add_argument("--password-store=basic")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.add_experimental_option(
        "prefs",
        {   
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }
    )

    driver = uc.Chrome(
        options=options,
        headless=headless,
        log_level=3,
        enable_cdp_events=usar_devtools  # habilitar devtools
    )

    if not headless:
        driver.maximize_window()
        if pos != "maximizada":
            ancho, alto = driver.get_window_size().values()
            if pos == "izquierda":
                driver.set_window_rect(x=0,y=0,width=ancho//2,height=alto)
            elif pos == "derecha":
                driver.set_window_rect(x=ancho//2,y=0,width=ancho//2,height=alto)

    return driver
