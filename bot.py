from discord import app_commands, Intents, Client, Interaction, File, Activity, ActivityType
import asyncio, time, base64, os
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from init_webdriver_uc import init_webdriver_ec

bot = Client(intents=Intents.default())
bot.tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await bot.change_presence(activity=Activity(type=ActivityType.playing, name="/help | Hexanot Bot"))
    await bot.tree.sync()
    print(f"✅ Bot conectado como {bot.user}")

async def generar_pdf_scribd(url: str, output_file: str = "documento.pdf"):
    driver = init_webdriver_ec(headless=True)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://documents-downloader.pages.dev/")
        time.sleep(2)

        try:
            e = wait.until(ec.element_to_be_clickable(((By.CSS_SELECTOR, "button.ant-modal-close"))))
            e.click()
        except:
            pass 

        e = wait.until(ec.element_to_be_clickable(((By.CSS_SELECTOR, "input.ant-input"))))
        e.send_keys(url)

        btn_on_send = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="button"]')))
        btn_on_send.click()
        time.sleep(2)

        driver.get("https://documents-downloader.pages.dev/document")
        time.sleep(3)


        driver.execute_script("""
            let marca = document.createElement('div');
            marca.innerText = '📄 Generado por ech0k';
            marca.style.position = 'fixed';
            marca.style.bottom = '30px';
            marca.style.left = '30px';
            marca.style.fontSize = '16px';
            marca.style.color = 'rgba(100, 100, 100, 0.6)';
            marca.style.fontFamily = 'Arial, sans-serif';
            marca.style.zIndex = '9999';
            document.body.appendChild(marca);
        """)

        pdf = driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})

        with open(output_file, "wb") as f:
            f.write(base64.b64decode(pdf['data']))

    finally:
        driver.quit()   

    return output_file

@bot.tree.command(name="scribd", description="Descargar documento de Scribd como PDF")
@app_commands.describe(enlace="Enlace al documento de Scribd")
async def scribd(interaction: Interaction, enlace: str):
    await interaction.response.defer(thinking=True)
    try:
        output_file = f"scribd_{int(time.time())}.pdf"
        await generar_pdf_scribd(enlace, output_file)
        await interaction.followup.send("✅ Documento generado con éxito:", file=File(output_file))
        os.remove(output_file)
    except Exception as e:
        await interaction.followup.send(f"❌ Error al procesar el documento:\n```\n{e}\n```")

bot.run("<TOKEN-DISCORD>")
