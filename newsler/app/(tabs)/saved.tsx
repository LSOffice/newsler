import {
  View,
  Text,
  Image,
  ScrollView,
  ActivityIndicator,
  ImageBackground,
  TouchableOpacity,
} from "react-native";
import React, { useEffect, useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import images from "../../constants/images";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { router } from "expo-router";
import Toast from "react-native-toast-message";

const Saved = () => {
  const [savedPosts, setSavedPosts] = useState([]);
  const [isLoaded, setisLoaded] = useState(false);
  const apiUrl = process.env.EXPO_PUBLIC_API_URL;
  const [savedArticles, setsavedArticles] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      if (isLoaded) {
        return;
      }
      try {
        let reloading = true;
        while (reloading) {
          const response = await fetch(apiUrl + "/articles/saved", {
            method: "POST",
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
              Authorization:
                "Bearer " + (await AsyncStorage.getItem("session_token")),
            },
            body: JSON.stringify({
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
          setSavedPosts(responseJson);
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

  if (!isLoaded) {
    return (
      <View className="w-full h-full flex justify-center items-center">
        <ActivityIndicator color="black" className="mb-3" />
      </View>
    );
  } else {
    return (
      <SafeAreaView className="w-full h-full bg-white flex-1">
        <View className="flex flex-col">
          <View className="flex flex-row items-center gap-2 justify-center">
            <Image
              source={images.logo}
              className="w-10 h-10"
              resizeMode="contain"
            />
            <Text className="text-2xl text-primary font-bold text-center">
              Newsler
            </Text>
          </View>

          <View className="flex flex-col mt-3">
            <Text className="text-2xl font-bold pl-4 mb-3">Saved Articles</Text>
            {savedPosts.length == 0 ? (
              <Text className="pl-4">
                You have no saved articles. Come back when you have!
              </Text>
            ) : (
              <ScrollView showsVerticalScrollIndicator={false}>
                {[...Array(Math.ceil(savedPosts.length / 4))].map(
                  (_, index) => (
                    <View key={index} className="flex flex-row">
                      {savedPosts
                        .slice(index * 4, index * 4 + 4)
                        .map((_, index1) => (
                          <TouchableOpacity
                            key={index * 4 + index1}
                            className="w-1/4 h-24 border border-white"
                            onPress={() =>
                              router.push(
                                "article/" +
                                  savedPosts[index * 4 + index1].article_id,
                              )
                            }
                          >
                            <ImageBackground
                              source={{
                                uri: savedPosts[index * 4 + index1].image_uri,
                              }}
                              className="w-full h-full flex flex-col"
                            >
                              {!savedPosts[index * 4 + index1].image_uri ? (
                                <Text className="mt-auto font-medium text-black">
                                  {savedPosts[index * 4 + index1].title}
                                </Text>
                              ) : (
                                <></>
                              )}
                            </ImageBackground>
                          </TouchableOpacity>
                        ))}
                    </View>
                  ),
                )}

                <View className="h-[150px]" />
              </ScrollView>
            )}
          </View>
        </View>
      </SafeAreaView>
    );
  }
};

export default Saved;
