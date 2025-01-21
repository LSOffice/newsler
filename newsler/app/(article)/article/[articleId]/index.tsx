// File that returns the article display page
// Path: /article/(articleId)

import {
  View,
  Text,
  ScrollView,
  Image,
  TouchableOpacity,
  SafeAreaView,
  Button,
  StatusBar,
  TextInput,
  Pressable,
  ActivityIndicator,
  Share,
} from "react-native";
import { Dialog, CheckBox, ListItem, Avatar } from "@rneui/themed";
import React, { useEffect, useRef, useState } from "react";
import {
  Link,
  router,
  useGlobalSearchParams,
  useLocalSearchParams,
  useNavigation,
} from "expo-router";
import images from "../../../../constants/images";
import {
  LucideBookmark,
  LucideChevronLeft,
  LucideCopyPlus,
  LucideFacebook,
  LucideGraduationCap,
  LucideHeart,
  LucideInstagram,
  LucideLinkedin,
  LucidePlane,
  LucideSend,
  LucideShare,
  LucideTwitch,
  LucideUpload,
  LucideUserCheck,
  LucideUserX,
} from "lucide-react-native";
import Toast from "react-native-toast-message";
import AsyncStorage from "@react-native-async-storage/async-storage";

// main object

const ArticleDisplay = () => {
  // Get Article ID from search parameters
  const local = useLocalSearchParams();
  const articleId = local.articleId;
  // setting local variables
  const [postSaved, setPostSaved] = useState(false);
  const [contentHeight, setContentHeight] = useState(0);
  const [newsArticle, setnewsArticle] = useState({});
  const [reactionInfo, setreactionInfo] = useState({});
  const apiUrl = process.env.EXPO_PUBLIC_API_URL;
  const [isLoaded, setisLoaded] = useState(false);
  const [runningSave, setrunningSave] = useState(false);
  const [timer, setTimer] = useState(0);
  const [greatestDepthTravelled, setgreatestDepthTravelled] = useState(0);
  const [reaction, setReaction] = useState(false);
  const [currentReaction, setcurrentReaction] = useState("");

  // Handles even when user leaves article (clicks left arrow button)
  const back = async () => {
    router.back();
    if (currentReaction != "") {
      let reaction_sentiment = 0.0;
      if (currentReaction == "love") {
        reaction_sentiment = 1.0;
      } else if (currentReaction == "smile") {
        reaction_sentiment = 0.75;
      } else if (currentReaction == "surprised") {
        reaction_sentiment = 0.5;
      } else if (currentReaction == "pensive") {
        reaction_sentiment = 0.3;
      }

      // saves article reaction data
      try {
        const response = await fetch(apiUrl + "/articles/reaction", {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization:
              "Bearer " + (await AsyncStorage.getItem("session_token")),
          },
          body: JSON.stringify({
            article_id: articleId,
            user_id: await AsyncStorage.getItem("userId"),
            reaction_sentiment: reaction_sentiment,
          }),
        });
      } catch (e) {
        Toast.show({
          type: "error",
          text1: "Error",
          text2: "An error occurred while saving reaction!",
          visibilityTime: 1000,
        });
      }
    }

    // saves article view and article scroll data
    try {
      const response = await fetch(apiUrl + "/articles/view", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization:
            "Bearer " + (await AsyncStorage.getItem("session_token")),
        },
        body: JSON.stringify({
          article_id: articleId,
          user_id: await AsyncStorage.getItem("userId"),
          view_seconds: timer,
          scroll_depth: greatestDepthTravelled / contentHeight,
        }),
      });
    } catch (e) {
      Toast.show({
        type: "error",
        text1: "Error",
        text2: "An error occurred while saving!",
        visibilityTime: 1000,
      });
    }
  };

  // Start timer that counts how long the user stays on the page for (view seconds)
  useEffect(() => {
    const intervalId = setInterval(() => {
      setTimer((prevTimer) => prevTimer + 1);
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

  // Handler to get the height of the content to determine scroll depth
  const handleContentSizeChange = (width, height) => {
    setContentHeight(height - 650);
  };

  // Handler for scroll event to determine scroll depth
  const handleScroll = async (e: any) => {
    e.persist();
    if (e.nativeEvent.contentOffset.y > greatestDepthTravelled) {
      setgreatestDepthTravelled(e.nativeEvent.contentOffset.y);
    }
  };

  // Set the reaction of the post by the user (locally)
  const reactionPost = async (reaction_sentiment: number) => {
    if (reaction) {
      Toast.show({
        type: "error",
        text1: "On cooldown",
        text2: "Reaction on cooldown",
        visibilityTime: 500,
      });
      return;
    }

    if (currentReaction != "") {
      if (reactionInfo[currentReaction] != 0) {
        reactionInfo[currentReaction] -= 1;
      }
    }
    if (reaction_sentiment == 1.0) {
      reactionInfo["love"] += 1;
      setcurrentReaction("love");
    } else if (reaction_sentiment == 0.75) {
      reactionInfo["smile"] += 1;
      setcurrentReaction("smile");
    } else if (reaction_sentiment == 0.3) {
      reactionInfo["pensive"] += 1;
      setcurrentReaction("pensive");
    } else if (reaction_sentiment == 0.5) {
      reactionInfo["surprised"] += 1;
      setcurrentReaction("surprised");
    } else if (reaction_sentiment == 0.0) {
      reactionInfo["angry"] += 1;
      setcurrentReaction("angry");
    }

    setreactionInfo(reactionInfo);
  };

  // save post event (making a request to toggle save - unsave or save)
  const savePost = async (e: any) => {
    if (runningSave) {
      return;
    }
    setrunningSave(true);
    setPostSaved(!postSaved);
    try {
      const response = await fetch(apiUrl + "/articles/save", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization:
            "Bearer " + (await AsyncStorage.getItem("session_token")),
        },
        body: JSON.stringify({
          article_id: articleId,
          user_id: await AsyncStorage.getItem("userId"),
          save: !postSaved,
        }),
      });

      if (response.ok) {
        if (!postSaved) {
          Toast.show({
            type: "success",
            text1: "Post saved!",
            text2: "View in your saved posts",
            onPress: () => router.push("/saved"),
            visibilityTime: 1000,
          });
        }
      } else {
        setPostSaved(!postSaved);
        Toast.show({
          type: "error",
          text1: "Error",
          text2: postSaved ? "Failed to unsave post!" : "Failed to save post!",
          visibilityTime: 1000,
        });
      }
      setrunningSave(false);
    } catch (e) {
      Toast.show({
        type: "error",
        text1: "Error",
        text2: postSaved ? "Failed to unsave post!" : "Failed to save post!",
        visibilityTime: 1000,
      });
    }
  };

  // Load article information when page starts
  useEffect(() => {
    const fetchData = async () => {
      if (isLoaded) {
        return;
      }
      try {
        let reloading = true;
        while (reloading) {
          const response = await fetch(apiUrl + "/articles/article", {
            method: "POST",
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
              Authorization:
                "Bearer " + (await AsyncStorage.getItem("session_token")),
            },
            body: JSON.stringify({
              article_id: articleId,
              user_id: await AsyncStorage.getItem("userId"),
            }),
          });
          if (response.status === 308) {
            const newResponse = await fetch(apiUrl + "/auth/refreshsession", {
              method: "POST",
              headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                refresh_token: await AsyncStorage.getItem("refresh_token"),
                user_id: await AsyncStorage.getItem("userId"),
              }),
            });
            const content = await newResponse.json();
            await AsyncStorage.setItem(
              "session_token",
              content["session_token"],
            );
            await AsyncStorage.setItem("email", content["email"]);
            continue;
          }
          const responseJson = await response.json();
          reloading = false;
          setnewsArticle(responseJson["article_info"]);
          setreactionInfo(responseJson["reaction_info"]["reactions"]);
          setcurrentReaction(responseJson["reaction_info"]["current_reaction"]);
          if (responseJson["reaction_info"]["post_saved"]) {
            setPostSaved(true);
          }
          setisLoaded(true);
        }
      } catch (e) {
        Toast.show({
          type: "error",
          text1: "Error",
          text2: "An error occurred",
          visibilityTime: 1000,
        });
      }
    };
    fetchData();
  }, []);

  // if page not loaded yet show loading circle spinner
  if (!isLoaded) {
    return (
      <View className="w-full h-full flex justify-center items-center">
        <TouchableOpacity className="absolute top-7 left-3" onPress={back}>
          <LucideChevronLeft size={28} className="text-black" />
        </TouchableOpacity>
        <ActivityIndicator color="black" className="mb-3" />
      </View>
    );
  } else {
    // else display article (HTML with tailwind classes)
    return (
      <SafeAreaView
        className="bg-white h-full w-full"
        style={{ flex: 1, paddingTop: StatusBar.currentHeight }}
      >
        <ScrollView
          onScroll={handleScroll}
          onContentSizeChange={handleContentSizeChange}
        >
          <View className="flex flex-row px-3 pt-2 items-center">
            <TouchableOpacity onPress={back}>
              <LucideChevronLeft size={28} className="text-black" />
            </TouchableOpacity>
            <View className="ml-auto">
              <View className="flex flex-row gap-1">
                <TouchableOpacity
                  onPress={async () => {
                    const result = await Share.share({
                      message:
                        "Check out this article on Newsler: " +
                        newsArticle.title,
                    });
                  }}
                >
                  <LucideSend size={32} className="text-primary" />
                </TouchableOpacity>
                <TouchableOpacity onPress={savePost}>
                  <LucideBookmark
                    fill={postSaved ? "#27576f" : "#FFF"}
                    size={32}
                    className="text-primary"
                  />
                </TouchableOpacity>
              </View>
            </View>
          </View>
          <View className="w-full h-full flex flex-col mt-3">
            {/* Article title element */}
            <View className="h-36 w-full flex flex-row items-center justify-center">
              <Image
                source={{ uri: newsArticle.image_uri }}
                className="w-11/12 h-36"
                resizeMode="cover"
              />
            </View>
            <View className="flex flex-col px-3 pt-3">
              <Text className="text-lg w-11/12 font-bold">
                {newsArticle.title}
              </Text>
              <View className="flex flex-row w-5/6 items-center pt-2">
                <Image
                  source={{
                    uri: "https://t4.ftcdn.net/jpg/06/08/55/73/360_F_608557356_ELcD2pwQO9pduTRL30umabzgJoQn5fnd.jpg",
                  }}
                  className="w-6 h-6 rounded-full"
                />
                <View className="flex flex-row items-center ml-2">
                  <Text className="mr-1 text-xs text-primary">
                    By {newsArticle.author}, {newsArticle.company}
                  </Text>
                  <TouchableOpacity>
                    {newsArticle.verified ? (
                      <LucideUserCheck size={20} className="text-primary" />
                    ) : (
                      <LucideUserX size={20} className="text-black" />
                    )}
                  </TouchableOpacity>
                </View>
                <Text className="text-primary ml-1">
                  {Math.floor(
                    (new Date().getTime() / 1000 - newsArticle.created_at) /
                      (24 * 60 * 60),
                  ) === 0
                    ? Math.floor(
                        (new Date().getTime() / 1000 - newsArticle.created_at) /
                          (60 * 60),
                      ) + "h"
                    : Math.floor(
                        (new Date().getTime() / 1000 - newsArticle.created_at) /
                          (24 * 60 * 60),
                      ) + "d"}
                </Text>
              </View>
              <Text className="mt-1 text-xs font-light">
                {/* 200 wpm is average reading time */}
                {(newsArticle.body.trim().split(/\s+/).length / 200).toFixed()}
                -minute read
              </Text>
              <View className="pt-3">
                <Text>{newsArticle.body}</Text>
              </View>
              <View className="py-3 flex flex-col">
                <View className="flex flex-row gap-2">
                  <TouchableOpacity
                    onPress={() => reactionPost(1.0)}
                    className="border border-red-600 py-2 px-1 rounded-2xl"
                  >
                    <Text className="text-sm">❤️ {reactionInfo["love"]}</Text>
                  </TouchableOpacity>
                  <TouchableOpacity
                    onPress={() => reactionPost(0.75)}
                    className="border border-yellow-400 py-2 px-1 rounded-2xl"
                  >
                    <Text className="text-sm">😂 {reactionInfo["smile"]}</Text>
                  </TouchableOpacity>
                  <TouchableOpacity
                    onPress={() => reactionPost(0.3)}
                    className="border border-yellow-400 py-2 px-1 rounded-2xl"
                  >
                    <Text className="text-sm">
                      😔 {reactionInfo["pensive"]}
                    </Text>
                  </TouchableOpacity>
                  <TouchableOpacity
                    onPress={() => reactionPost(0.5)}
                    className="border border-yellow-400 py-2 px-1 rounded-2xl"
                  >
                    <Text className="text-sm">
                      😲 {reactionInfo["surprised"]}
                    </Text>
                  </TouchableOpacity>
                  <TouchableOpacity
                    onPress={() => reactionPost(0.0)}
                    className="border border-orange-600 py-2 px-1 rounded-2xl"
                  >
                    <Text className="text-sm">😡 {reactionInfo["angry"]}</Text>
                  </TouchableOpacity>
                </View>
              </View>
            </View>
          </View>
        </ScrollView>
      </SafeAreaView>
    );
  }
};

export default ArticleDisplay;
