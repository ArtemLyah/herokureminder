from configparser import ConfigParser
import db

class Localisation:
    def __init__(self) -> None:
        self.languages = ["english", "russian"]
        self.parser = ConfigParser()      
    def __configure(self, text:str):
        text = text.replace("\\n", "\n")
        return text

    def get(self, user_id, code_word):
        lang_id = int(db.get_from_user_settings(user_id, ["localisation"]))
        lang = self.languages[lang_id]
        self.parser.read(f"localisation/{lang}.ini", encoding='utf-8')
        return self.__configure(self.parser.get("language", code_word))

    def set_for_user(self, user_id):
        lid = int(db.get_from_user_settings(user_id, ["localisation"]))
        db.set_user_settings(user_id, localisation=(lid+1)%len(locale.languages))
        
locale = Localisation()
