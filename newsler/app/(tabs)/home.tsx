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

const Home = () => {
  const [isRefresh, setisRefresh] = useState(false);
  const [dataSource, setDataSource] = useState([{}]);
  const [offset, setOffset] = useState(1);
  const [isListEnd, setIsListEnd] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [yOffset, setyOffset] = useState(0);

  useEffect(() => {
    getData();
  }, []);

  useEffect(() => {
    if (isRefresh) {
      setDataSource([]);
      console.log("isRefresh");
      fetch("https://dummyjson.com/products?offset=" + offset)
        .then((response) => response.json())
        .then((data) => {
          if (data.products.length > 0) {
            setOffset(offset + 1);
            if (selectedIndex == 0) {
              setDataSource([...newsArticles]);
            } else {
              setDataSource([]);
            }
          } else {
            setDataSource([]);
            setIsListEnd(true);
          }
          setisRefresh(false);
        })
        .catch((error) => {
          console.error(error);
        });
    }
  }, [isRefresh]);

  const numOfTabs = 4;
  const NavigationTabs = [
    {
      id: 0,
      name: "Trending",
    },
    {
      id: 1,
      name: "Hong Kong",
    },
    {
      id: 2,
      name: "Sports",
    },
    {
      id: 3,
      name: "Politics",
    },
    {
      id: 4,
      name: "Pop Culture",
    },
  ];

  let newsArticles = [
    {
      article_id: "abc",
      title: "Island School unveils new billion-dollar campus",
      author: "Lorem Ipsum",
      company: "BBC",
      verified: true,
      live: true,
      image_uri:
        "https://island.edu.hk/wp-content/uploads/2022/08/NAM_0019.jpg",
    },
    {
      article_id: "abcd",
      title: "Biden seeking re-election in 2024",
      author: "Lorem Ipsum",
      company: "BBC",
      verified: true,
      live: false,
      image_uri:
        "https://cdn.britannica.com/66/226766-138-235EFD92/who-is-President-Joe-Biden.jpg?w=800&h=450&c=crop",
    },
    {
      article_id: "abcde",
      title: "GTA VI Trailer out: Much to look forward to?",
      author: "Jeff Bob",
      company: "Tailor News",
      verified: false,
      live: false,
      image_uri:
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVA7faN3W4oHcL_WF5sUYtMdBDjMld_erQuQ&s",
    },
    {
      article_id: "abcde",
      title: "GTA VI Trailer out: Much to look forward to?",
      author: "Jeff Bob",
      company: "Tailor News",
      verified: false,
      live: false,
      image_uri:
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVA7faN3W4oHcL_WF5sUYtMdBDjMld_erQuQ&s",
    },
  ];

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

  const getData = () => {
    if (!isRefresh) {
      setisRefresh(true);
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
      >
        <View className="h-full flex flex-col">
          <Image
            source={{ uri: item.image_uri }}
            className="w-full h-full rounded-2xl absolute"
          />
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
      >
        <View className="h-3/4">
          <Image
            source={{ uri: item.image_uri }}
            className="w-full h-full rounded-t-2xl"
          />
        </View>
        <View className="h-1/4 bg-gray-200 rounded-b-2xl px-3 flex flex-col justify-center">
          <Text numberOfLines={1} className="text-base font-medium">
            {item.title}
          </Text>
          <View className="flex flex-row gap-1 items-center">
            <Text className="text-xs font-light">
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

  const handleScroll = (e: any) => {
    // To mimic effect of infinite scroll
    if (
      e.nativeEvent.contentOffset.y > yOffset &&
      e.nativeEvent.contentOffset.y > 0 &&
      yOffset > 0
    ) {
      // when scrolling down
      console.log(e.nativeEvent.contentOffset.y);
      console.log(yOffset);
      if (!isRefresh) {
        setDataSource([
          ...dataSource,
          {
            article_id: "abcde",
            title: "GTA VI Trailers out: Much to look forward to?",
            author: "Jeff Bob",
            company: "Tailor News",
            verified: false,
            live: false,
            image_uri:
              "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVA7faN3W4oHcL_WF5sUYtMdBDjMld_erQuQ&s",
          },
        ]);
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
        <HorizontalScrollMenu
          items={NavigationTabs}
          onPress={onPress}
          selected={selectedIndex}
          activeBackgroundColor={`${selectedIndex == 0 ? "#FCA311" : "#275F6F"}`}
          activeTextColor={`${selectedIndex == 0 ? "black" : "white"}`}
          buttonStyle={{
            borderColor: "white",
          }}
          textStyle={{
            color: "#275F6F",
          }}
        />
      </View>

      {
        <View>
          {isRefresh ? (
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
            <Text className="ml-3 text-base font-semibold">James Baker</Text>
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
            <TouchableOpacity className="border-2 mt-1 py-2 px-3 rounded-2xl border-red-600">
              <Text className="text-base text-red-600">Delete account</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Dialog>

      <FlatList
        showsVerticalScrollIndicator={false}
        data={dataSource}
        keyExtractor={(item, index) => index.toString()}
        ItemSeparatorComponent={ItemSeperatorView}
        renderItem={ItemView}
        className="px-4"
        onScroll={handleScroll}
      />
    </SafeAreaView>
  );
};

export default Home;
