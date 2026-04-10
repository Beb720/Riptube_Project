import json

class Config:
    def __init__(self):
        with open("config.json", "r") as f:
            self.config_data = json.load(f)

    def save(self):
        with open("config.json", "w") as f:
            json.dump(self.config_data, f, indent=4)
    
    def reset(self):
        config = self.config_data["config"]
        base = self.config_data["base_settings"]
        for key in config:
            config[key] = base[key]
        self.save()

    def veiw_settings(self):
        settings = ["SETTINGS:"]
        for key in self.config_data['config']:
            settings.append(f'\t{key}: {self.config_data['config'][key]}')
        return settings

    def setting_options(self):
        options = []
        for key in self.config_data['config']:
            options.append(key)
        return options
    
    def change_setting(self, setting, orig_value):
        conversion = {'str': str, 'int': int, 'bool': bool}
        
        expected_type = self.config_data['config_types'][setting]
        
        # Convert based on the expected type
        try:
            new_value = conversion[expected_type](orig_value)
        except (ValueError, TypeError):
            print('ERROR: Could not convert value')
            return
        

        if str(type(new_value).__name__) == expected_type:
            self.config_data['config'][setting] = new_value
            self.save()
            print('Setting changed.')

        else:
            print('ERROR: That is not a valid input for that setting')
            print(f"'{setting}' requires a {expected_type}")