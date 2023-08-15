import json



with open("Settings/instrument_controller_settings.txt", "r") as text_file:
    settings_dict = json.load(text_file)

settings_dict["wavelength_step"] = 1560

with open("Settings/instrument_controller_settings.txt", "w") as text_file:
    json.dump(settings_dict, text_file)
