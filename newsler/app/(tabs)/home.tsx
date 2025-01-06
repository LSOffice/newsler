import {
  View,
  Text,
  ScrollView,
  FlatList,
  ActivityIndicator,
  Image,
  TouchableOpacity,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import React, { useEffect, useState } from "react";
import images from "../../constants/images";
import {
  Bell,
  LucideBell,
  LucideHome,
  LucideLocate,
  LucideMenu,
  LucidePanelTop,
  LucideUser,
  LucideVerified,
  UserCheck,
  UserX,
} from "lucide-react-native";
import BlinkDot from "../../components/Blink";
import HorizontalScrollMenu, {
  RouteProps,
} from "@nyashanziramasanga/react-native-horizontal-scroll-menu/src";
import { router } from "expo-router";
import { Dialog } from "@rneui/themed";
import AsyncStorage from "@react-native-async-storage/async-storage";
import Toast from "react-native-toast-message";

const Home = () => {
  const [isRefresh, setisRefresh] = useState(false);
  const [dataSource, setDataSource] = useState([{}]);
  const [offset, setOffset] = useState(0);
  const [isListEnd, setIsListEnd] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(1);
  const [yOffset, setyOffset] = useState(0);
  const [loadingNewPage, setloadingNewPage] = useState(false);
  const [preventOnce, setPreventOnce] = useState(false);
  const [navigationTabs, setNavigationTabs] = useState([]);
  const [isLoading, setisLoading] = useState(false);
  const [userId, setuserId] = useState("");

  const apiUrl = process.env.EXPO_PUBLIC_API_URL;

  const getData = () => {
    if (!isRefresh) {
      setisRefresh(true);
    }
  };

  useEffect(() => {
    getData();
    const fetchData = async () => {
      setuserId(await AsyncStorage.getItem("userId"));
      try {
        let loading = true;
        while (loading) {
          setisLoading(true);
          setNavigationTabs([]);
          const response = await fetch(apiUrl + "/articles/headers", {
            method: "POST",
            headers: {
              Accept: "application/json",
              Authorization:
                "Bearer " + (await AsyncStorage.getItem("session_token")),
              "Content-Type": "application/json",
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
            continue;
          }
          loading = false;
          const responseJson = await response.json();
          let count = 0;
          for (let header of responseJson) {
            navigationTabs.push({
              id: count,
              name: header,
            });
            count++;
          }
          setNavigationTabs(navigationTabs);
          setisLoading(false);
        }
      } catch (e) {
        console.error(e);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      if (isRefresh) {
        setDataSource([]);
        Toast.show({
          type: "info",
          visibilityTime: 5000,
          position: "bottom",
          text1: "Your internet connection is slow",
          text2: "Loading will take a while",
        });
        try {
          let loading = true;
          while (loading) {
            console.log(new Date().getTime() / 1000);
            const response = await fetch(apiUrl + "/articles/feed", {
              method: "POST",
              headers: {
                Accept: "application/json",
                Authorization:
                  "Bearer " + (await AsyncStorage.getItem("session_token")),
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                user_id: await AsyncStorage.getItem("userId"),
                topic: "Trending",
                page: 1,
              }),
            });
            console.log(new Date().getTime() / 1000);
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
            loading = false;
            const responseJson = await response.json();
            setDataSource([...responseJson]);
            setisRefresh(false);
            setOffset(0);
            setloadingNewPage(false);
          }
        } catch (e) {
          console.error(e);
        }
      }
    };
    fetchData();
  }, [isRefresh]);

  const onPress = (route: RouteProps) => {
    setSelectedIndex(route.id);
    getData();
  };

  const showDataSource = () => {
    if (selectedIndex == 0) {
      setDataSource([...newsArticles]);
    } else {
      setDataSource([]);
    }
  };

  const ItemView = ({
    item,
  }: {
    item: {
      author: string;
      company: string;
      image_uri: string;
      title: string;
      verified: boolean;
      article_id: string;
      live: boolean;
    };
  }) => {
    return item.live ? (
      <TouchableOpacity
        onPress={() => getItem(item)}
        className="border-[0.5px] rounded-2xl border-tertiary flex flex-col h-56"
        key={item.article_id}
      >
        <View className="h-full flex flex-col">
          {item.image_uri ? (
            <Image
              source={{ uri: item.image_uri }}
              className="w-full h-full rounded-t-2xl"
            />
          ) : (
            <Image
              source={{ uri: null }}
              className="w-full h-full rounded-t-2xl"
            />
          )}
          <View className="flex flex-row items-center p-3">
            <BlinkDot duration={2000}>
              <View className="rounded-2xl w-3 h-3 bg-red-700" />
            </BlinkDot>
            <Text className="ml-2 text-xs text-white font-bold">
              Live updates
            </Text>
          </View>
          <Text
            numberOfLines={2}
            className="mt-auto pl-3 pb-1 text-base text-white font-medium"
          >
            {item.title}
          </Text>
        </View>
      </TouchableOpacity>
    ) : (
      <TouchableOpacity
        onPress={() => getItem(item)}
        className="border-[0.5px] rounded-2xl border-tertiary flex flex-col h-48"
        key={item.article_id}
      >
        <View className="h-3/4">
          {item.image_uri ? (
            <Image
              source={{ uri: item.image_uri }}
              className="w-full h-full rounded-t-2xl"
            />
          ) : (
            <Image
              source={{ uri: null }}
              className="w-full h-full rounded-t-2xl"
            />
          )}
        </View>
        <View className="h-1/4 bg-gray-200 rounded-b-2xl px-3 flex flex-col justify-center">
          <Text numberOfLines={1} className="text-sm font-medium">
            {item.title}
          </Text>
          <View className="flex flex-row gap-1 items-center">
            <Text numberOfLines={1} className="text-xs font-light w-11/12">
              By {item.author}, {item.company}
            </Text>
            {item.verified ? (
              <UserCheck size={14} className="text-primary" />
            ) : (
              <UserX size={14} className="text-black" />
            )}
          </View>
        </View>
      </TouchableOpacity>
    );
  };

  const ItemSeperatorView = () => {
    return <View className="h-5"></View>;
  };

  const getItem = (item: {
    author: string;
    company: string;
    image_uri: string;
    title: string;
    verified: boolean;
    article_id: string;
    live: boolean;
  }) => {
    router.push("article/" + item.article_id);
  };
  const getRandomInt = (max: number) => {
    return Math.floor(Math.random() * max);
  };

  const handleScroll = async (e: any) => {
    e.persist();
    // To mimic effect of infinite scroll
    if (
      e.nativeEvent.contentOffset.y > yOffset &&
      e.nativeEvent.contentOffset.y > 0 &&
      yOffset > 0
    ) {
      setPreventOnce(true);
      if (e.nativeEvent.contentOffset.y >= 1700 && offset == 0) {
        setOffset(1);
        try {
          let reloading = true;
          while (reloading) {
            const response = await fetch(apiUrl + "/articles/feed", {
              method: "POST",
              headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                Authorization:
                  "Bearer " + (await AsyncStorage.getItem("session_token")),
              },
              body: JSON.stringify({
                user_id: await AsyncStorage.getItem("userId"),
                topic: "Trending",
                page: 2,
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
            setDataSource([...dataSource, ...responseJson]);
            reloading = false;
          }
        } catch (e) {
          console.error(e);
        }
      } else if (
        e.nativeEvent.contentOffset.y >= 1700 + offset * 1000 &&
        !loadingNewPage
      ) {
        setloadingNewPage(true);
        const offsetValue = offset;
        setOffset(offsetValue + 1);
        try {
          let reloading = true;
          while (reloading) {
            const response = await fetch(apiUrl + "/articles/feed", {
              method: "POST",
              headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                Authorization:
                  "Bearer " + (await AsyncStorage.getItem("session_token")),
              },
              body: JSON.stringify({
                user_id: await AsyncStorage.getItem("userId"),
                topic: "Trending",
                page: offsetValue + 2,
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
            setDataSource([...dataSource, ...responseJson]);
            reloading = false;
          }
        } catch (e) {
          console.error(e);
        }
      }
    } else {
      // going up
      if (yOffset < -10) {
        if (preventOnce) {
          // first scroll up doesn't immediately reload
          setTimeout(() => setPreventOnce(false), 500);
        } else {
          setisRefresh(true);
        }
      }
    }

    setyOffset(e.nativeEvent.contentOffset.y);
  };

  const [userDialogVisible, setUserDialogVisible] = useState(false);

  return (
    <SafeAreaView className="bg-white h-full w-full flex-1">
      <View className="flex flex-col gap-3 mb-2">
        <View className="border-b-[0.5px] pb-2 border-tertiary px-4">
          <View className="flex flex-row w-full justify-center items-center">
            <TouchableOpacity
              className="mr-auto"
              onPress={() => {
                setUserDialogVisible(true);
              }}
            >
              <Image
                source={{
                  uri: "https://t4.ftcdn.net/jpg/06/08/55/73/360_F_608557356_ELcD2pwQO9pduTRL30umabzgJoQn5fnd.jpg",
                }}
                className="w-10 h-10 rounded-full"
              />
            </TouchableOpacity>

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
            <TouchableOpacity className="ml-auto" onPress={() => {}}>
              <LucideBell size={32} className="text-primary" />
            </TouchableOpacity>
          </View>
        </View>
        <View className="flex flex-row items-center">
          {isLoading ? (
            <></>
          ) : (
            <HorizontalScrollMenu
              items={navigationTabs}
              onPress={onPress}
              selected={selectedIndex}
              activeBackgroundColor={`${selectedIndex == 1 ? "#FCA311" : "#275F6F"}`}
              activeTextColor={`${selectedIndex == 1 ? "black" : "white"}`}
              buttonStyle={{
                borderColor: "white",
                minWidth: 105,
              }}
              textStyle={{
                color: "#275F6F",
              }}
            />
          )}
        </View>
      </View>

      {
        <View>
          {isRefresh || isLoading ? (
            <ActivityIndicator color="black" className="mb-3" />
          ) : null}
        </View>
      }
      <Dialog
        isVisible={userDialogVisible}
        onBackdropPress={() => setUserDialogVisible(!userDialogVisible)}
      >
        <View className="flex flex-col">
          <View className="flex flex-row items-center">
            <Image
              source={{
                uri: "https://t4.ftcdn.net/jpg/06/08/55/73/360_F_608557356_ELcD2pwQO9pduTRL30umabzgJoQn5fnd.jpg",
              }}
              className="w-8 h-8 rounded-full"
            />
            <Text className="ml-3 text-base font-semibold">{userId}</Text>
            <View className="ml-auto flex flex-row">
              <Image
                source={images.logo}
                className="w-8 h-8"
                resizeMode="contain"
              />
              <Text className="mt-auto text-primary text-xs">PRO</Text>
            </View>
          </View>
          <View className="flex flex-col mt-2">
            <TouchableOpacity className="border-2 mt-1 py-2 px-3 rounded-2xl">
              <Text className="text-base">Change email</Text>
            </TouchableOpacity>
            <TouchableOpacity className="border-2 mt-1 py-2 px-3 rounded-2xl">
              <Text className="text-base">Change password</Text>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={async () => {
                await AsyncStorage.removeItem("session_token");
                await AsyncStorage.removeItem("refresh_token");
                await AsyncStorage.removeItem("userId");
                setUserDialogVisible(false);
                router.push("/login");
              }}
              className="border-2 mt-1 py-2 px-3 rounded-2xl border-red-600"
            >
              <Text className="text-base text-red-600">Log-out</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Dialog>

      {isLoading ? (
        <></>
      ) : (
        <FlatList
          showsVerticalScrollIndicator={false}
          data={dataSource}
          keyExtractor={(item, index) => index.toString()}
          ItemSeparatorComponent={ItemSeperatorView}
          renderItem={ItemView}
          className="px-4"
          onScroll={handleScroll}
        />
      )}
    </SafeAreaView>
  );
};

export default Home;
