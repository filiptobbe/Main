
#Skapar klassen "TV"
class TV:

    #Skapar instansvariablerna
    def __init__(self, tv_name_input, max_channel_input, current_channel_input, max_volume_input, current_volume_input):
        self.tv_name = tv_name_input

        self.max_channel = max_channel_input
        self.current_channel = current_channel_input

        self.max_volume = max_volume_input
        self.current_volume = current_volume_input
        

    #Byter kanal om talet är mindre än max_channel och större än 0
    def change_channel(self, new_channel):
        if new_channel > 0 and new_channel <= self.max_channel:
            self.current_channel = new_channel
            return True
        else:
            return False
    
    #Höjer volymen om den är mindre än max_volume
    def increase_volume(self):
        if self.current_volume + 1 <= self.max_volume:
            self.current_volume += 1
            return True
        else:
            return False
        
    #Sänker volymen om den är större än 0
    def decrease_volume(self):
        if self.current_volume - 1 >= 0:
            self.current_volume -= 1
            return True
        else:
            return False
    
    def __str__(self):
        return f"{self.tv_name}, channel: {self.current_channel}, volume: {self.current_volume}"
    
    def str_for_file(self):
            return f"{self.tv_name}, {self.max_channel}, {self.current_channel}, {self.max_volume}, {self.current_volume}"

  
"""
tv = TV("Vardagsrums TV", 100, 22, 10, 9)
tv2 = TV("Sovrums TV", 50, 7, 20, 4)"""