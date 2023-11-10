import instaloader

class Save_and_get_Details:
    def __init__(self, url , ):
        self.url = url
        self.username = "behruz.beg"
        self.inst = instaloader.Instaloader()
        self.video_url = ""

    def __login(self):
        self.inst.load_session_from_file(self.username)

    def __get_only_code(self):
        link = self.url
        s = 0
        link_code = ""
        for word in self.url:
            if word == "/" and s != 4:
                s += 1
            elif s == 4:
                if word == "/":
                    break
                link_code += word
        return link_code

    def get_post_detaile(self):
        details = [
            self.postt.title ,
            self.postt.likes,
            self.postt.comments,
            self.postt.caption,        #self.postt.caption_hashtags,
            self.postt.date,

        ]
        return details

    def save_post(self):
        self.__login()
        post = instaloader.Post.from_shortcode(
            self.inst.context, self.__get_only_code()
        )
        info = {
            "title": post.title,
            "likes": post.likes,
            "comments": post.comments,
            "date ": post.date.date(),
        }
        self.postt = post
        self.video_url = post.video_url
        return post.video_url


class Get_Profile_Info:
    def __init__(self, sesion, username):
        self.username = username
        self.sesion = sesion
        self.inst = instaloader.Instaloader()

    def __login(self):
        self.inst.load_session_from_file(self.sesion)

    def get_posts(self):
        self.__login()
        profile = instaloader.Profile.from_username(self.inst.context, self.username)
        self.profile_info = profile

    def posts_filter(self):
        profile = self.profile_info
        biografiya = profile.biography

        posts = profile.get_posts()

        # 

        maxin = 0
        minin = 100_000 
        followers = profile.followers
        following = profile.followees
        likes_ob = 0
        coments_ob = 0
        tim = 0
        post_count = posts.count

        for post in posts:

            # Getting max and min likes of post

            if post.likes > maxin:
                maxin = post.likes
            if post.likes < minin:
                minin = post.likes

            # Getting info posts

            likes_ob += post.likes
            coments_ob += post.comments

            tim += int(str(post.date)[11:13])
            # tim += int(timee)
        max_post = ""
        min_post = ""

        # print("[ INFO ] | PROGRESING |")
        for result in profile.get_posts():
            if result.likes == maxin and max_post == '':
                # print(result.shortcode)
                max_post += "https://www.instagram.com/p/" + result.shortcode
            elif result.likes == minin and min_post == '':
                # print(result.shortcode)
                min_post += "https://www.instagram.com/p/" + result.shortcode

        # print("[ INFO ] | END FOR |")

        # Response V 

        response = {
            "profile": {
                "biografiya": biografiya,
                "followers": followers,
                "following": following,
            },
            "posts": {
                "max_post": {
                    "likes": maxin,
                    "link": max_post,
                },
                "min_post": {
                    "likes": minin,
                    "link": min_post,
                },
            },
            "info" : {
                'midle_likes' : int(likes_ob / post_count),
                'midle_coments' : int(coments_ob / post_count) + 1,
                'post_time_day1' : (int((tim / post_count) + 6 )%24),
                'post_time_day2' : (int((tim / post_count))%24)
            }
        }
        return response
