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
} from "react-native";
import { Dialog, CheckBox, ListItem, Avatar } from "@rneui/themed";
import React, { useEffect, useState } from "react";
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

const ArticleDisplay = () => {
  const local = useLocalSearchParams();
  const articleId = local.articleId;
  const [isModalVisible, setModalVisible] = useState(false);
  const [postSaved, setPostSaved] = useState(false);
  const toggleModal = () => {
    setModalVisible(!isModalVisible);
  };
  const [newsArticle, setnewsArticle] = useState({});
  const [reactionInfo, setreactionInfo] = useState({});
  const apiUrl = process.env.EXPO_PUBLIC_API_URL;
  const [isLoaded, setisLoaded] = useState(false);
  const [runningSave, setrunningSave] = useState(false);
  const [timer, setTimer] = useState(0);

  const back = async () => {
    router.back();
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

  useEffect(() => {
    const intervalId = setInterval(() => {
      setTimer((prevTimer) => prevTimer + 1);
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

  const setReaction = async (e: any) => {
    if (runningSave) {
      return;
    }
    setrunningSave(true);
    Toast.show({
      type: "info",
      text1: postSaved ? "Unsaving post!" : "Saving post!",
      text2: "Give it a bit...",
      visibilityTime: 200000,
    });
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
      const responseJson = await response.json();
      if (responseJson) {
        setPostSaved(!postSaved);
        Toast.show({
          type: "success",
          text1: postSaved ? "Post unsaved!" : "Post saved!",
          text2: postSaved ? "" : "View in your saved posts",
          visibilityTime: 1000,
        });
      } else {
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

  const savePost = async (e: any) => {
    if (runningSave) {
      return;
    }
    setrunningSave(true);
    Toast.show({
      type: "info",
      text1: postSaved ? "Unsaving post!" : "Saving post!",
      text2: "Give it a bit...",
      visibilityTime: 200000,
    });
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
      const responseJson = await response.json();
      if (responseJson) {
        setPostSaved(!postSaved);
        Toast.show({
          type: "success",
          text1: postSaved ? "Post unsaved!" : "Post saved!",
          text2: postSaved ? "" : "View in your saved posts",
          visibilityTime: 1000,
        });
      } else {
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

  useEffect(() => {
    const fetchData = async () => {
      if (isLoaded) {
        return;
      }
      try {
        let reloading = true;
        while (reloading) {
          console.log(new Date().getTime() / 1000);
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
            continue;
          }
          const responseJson = await response.json();
          reloading = false;
          console.log(responseJson);
          setnewsArticle(responseJson["article_info"]);
          for (let reaction of responseJson["reaction_info"]) {
            if (reaction["interaction"] == 5) {
              setPostSaved(true);
            }
          }
          setreactionInfo(responseJson["reaction_info"]);
          setisLoaded(true);
        }
      } catch (e) {
        console.log(e);
      }
    };
    fetchData();
  }, []);

  if (!isLoaded) {
    return (
      <View className="w-full h-full flex justify-center items-center">
        <ActivityIndicator color="black" className="mb-3" />
      </View>
    );
  } else {
    return (
      <SafeAreaView
        className="bg-white h-full w-full"
        style={{ flex: 1, paddingTop: StatusBar.currentHeight }}
      >
        <ScrollView>
          <View className="flex flex-row px-3 pt-2 items-center">
            <TouchableOpacity onPress={back}>
              <LucideChevronLeft size={28} className="text-black" />
            </TouchableOpacity>
            <View className="ml-auto">
              <View className="flex flex-row gap-1">
                <TouchableOpacity onPress={toggleModal}>
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
                  <TouchableOpacity className="border border-red-600 py-2 px-1 rounded-2xl">
                    <Text className="text-sm">❤️ 120</Text>
                  </TouchableOpacity>
                  <TouchableOpacity className="border border-yellow-400 py-2 px-1 rounded-2xl">
                    <Text className="text-sm">😂 120</Text>
                  </TouchableOpacity>
                  <TouchableOpacity className="border border-yellow-400 py-2 px-1 rounded-2xl">
                    <Text className="text-sm">😔 120</Text>
                  </TouchableOpacity>
                  <TouchableOpacity className="border border-yellow-400 py-2 px-1 rounded-2xl">
                    <Text className="text-sm">😲 120</Text>
                  </TouchableOpacity>
                  <TouchableOpacity className="border border-orange-600 py-2 px-1 rounded-2xl">
                    <Text className="text-sm">😡 120</Text>
                  </TouchableOpacity>
                </View>
                <View className="flex flex-col pt-2 gap-1">
                  <Text className="text-primary text-lg">Comments</Text>
                  <TextInput
                    editable
                    multiline
                    numberOfLines={4}
                    maxLength={40}
                    // onChangeText={text => onChangeText(text)}
                    // value={value}
                    className="border px-3 py-2 rounded-xl"
                  />
                </View>
              </View>
            </View>
          </View>
        </ScrollView>

        <Dialog isVisible={isModalVisible} onBackdropPress={toggleModal}>
          <View className="flex flex-col w-full">
            <Text className="text-lg font-bold">Share to</Text>
            <View className="flex flex-row items-center justify-center mt-2 gap-3">
              <LucideFacebook className="text-primary" />
              <LucideInstagram className="text-primary" />
              <LucideTwitch className="text-primary" />
              <LucideLinkedin className="text-primary" />
            </View>
            <View className="flex flex-col items-center mt-2">
              <Pressable className="items-center mt-2 flex flex-row border w-full p-2 border-dotted border-primary rounded-2xl">
                <LucideGraduationCap className="mr-3 text-primary" />
                <Text className="text-sm flex-shrink">
                  Add article onto [classroom] stream
                </Text>
              </Pressable>
              <Pressable className="items-center mt-2 flex flex-row border w-full p-2 border-dotted border-primary rounded-2xl">
                <LucideGraduationCap className="mr-3 text-primary" />
                <Text className="text-sm flex-shrink">
                  Add article onto [classroom2] stream
                </Text>
              </Pressable>
              <Pressable className="items-center mt-2 flex flex-row border w-full p-2 border-dotted border-primary rounded-2xl">
                <LucideCopyPlus className="mr-3 text-primary" />
                <Text className="text-sm flex-shrink">
                  Add article onto [classroom] assignments
                </Text>
              </Pressable>
            </View>
          </View>
        </Dialog>
      </SafeAreaView>
    );
  }
};

export default ArticleDisplay;
