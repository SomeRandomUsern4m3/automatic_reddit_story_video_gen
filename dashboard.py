import os
import customtkinter as ctk
import time
import video_maker
import reddit_scraper
import threading




class Program(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x250")
        if not os.path.isdir("./game_footage"):
            os.mkdir("./game_footage")
        self.reddit_related_frame = ctk.CTkFrame(self)
        self.reddit_related_frame.pack(side="top", pady=10)
        self.reddit_scraping_frame = ctk.CTkFrame(self.reddit_related_frame)
        self.reddit_scraping_frame.pack(side="left", pady=10, padx=10)
        self.reddit_video_making_frame = ctk.CTkFrame(self.reddit_related_frame)
        self.reddit_video_making_frame.pack(side="left", pady=10, padx=10)

        #reddit scraping apparatus
        self.reddit_scraper_title = ctk.CTkLabel(self.reddit_scraping_frame, text="Reddit Scraping", font=("Arial", 16))
        self.reddit_scraper_title.pack(side="top", pady=10, padx=10)
        self.reddit_scraper_desc = ctk.CTkLabel(self.reddit_scraping_frame, text="The higher the scroll number the more stories are captured I reccomend at least 20", font=("Arial", 12))
        self.reddit_scraper_desc.pack(side="top", pady=10, padx=10)

        
        self.scroll_value_box = ctk.CTkEntry(self.reddit_scraping_frame, width=200, placeholder_text="Enter a integer(number)")
        self.scroll_value_box.pack(side="top", pady=10)

        self.reddit_scrape_button = ctk.CTkButton(self.reddit_scraping_frame, text="Scrape!", command=self.scrape)
        self.reddit_scrape_button.pack(side="top", pady=10, padx=10)


        #video making apparatus
        self.reddit_video_making_title = ctk.CTkLabel(self.reddit_video_making_frame, text="Make reddit videos here, a few options are available", font=("Arial", 16))
        self.reddit_video_making_title.pack(side="top", pady=10, padx=10)
        
        
        self.reddit_video_optionmenu = ctk.CTkOptionMenu(self.reddit_video_making_frame,values=["Randomly Pick Stories", "Loop Through All Stories"])
        self.reddit_video_optionmenu.set("Randomly Pick Stories")
        self.reddit_video_optionmenu.pack(side="top", pady=10, padx=10)

        self.reddit_video_subtitle_option = ctk.CTkSwitch(self.reddit_video_making_frame, text="Subtitles")
        self.reddit_video_subtitle_option.pack(side="top", pady=10, padx=10)

        self.make_reddit_video_button = ctk.CTkButton(self.reddit_video_making_frame, text="Make Video", command=self.make_video)
        self.make_reddit_video_button.pack(side="top", pady=10, padx=10)

        self.mainloop()
    def thread_for_making_random_videos(self):
        video_maker.make_video(subtitles=self.tmp_subtitles_val)
        self.make_reddit_video_button.configure(state="normal")
    def thread_for_making_all_videos(self):
        self.all_stories = os.listdir(os.path.abspath("./stories/"))
        for i in self.all_stories:
            video_maker.make_video(i, subtitles=self.tmp_subtitles_val)
        self.make_reddit_video_button.configure(state="normal")
    def make_video(self):
        self.tmp_optionmenu_val = self.reddit_video_optionmenu.get()
        self.tmp_subtitles_val = bool(int(self.reddit_video_subtitle_option.get()) == 1)
        
        if self.tmp_optionmenu_val == "Loop Through All Stories":
            self.thread_2 = threading.Thread(target=self.thread_for_making_random_videos)
            self.thread_2.start()
            self.make_reddit_video_button.configure(state="disabled")
        else:
            self.thread_1 = threading.Thread(target=self.thread_for_making_random_videos)
            self.thread_1.start()
            self.make_reddit_video_button.configure(state="disabled")
    def thread_for_scrape(self):
        self.scroll_value = int(self.scroll_value_box.get())
        if self.scroll_value < 7:
            print("defaulting to 20")
            self.scroll_value = 7
        reddit_scraper.scrape_reddit(scroll_amount=self.scroll_value)
        self.reddit_scrape_button.configure(state="normal")
    def scrape(self):
        self.thread_3 = threading.Thread(target=self.thread_for_scrape)
        self.thread_3.start()
        self.reddit_scrape_button.configure(state="disabled")
Program()
