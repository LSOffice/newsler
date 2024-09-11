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
} from "react-native";
import { Dialog, CheckBox, ListItem, Avatar } from "@rneui/themed";
import React, { useState } from "react";
import {
  Link,
  router,
  useGlobalSearchParams,
  useLocalSearchParams,
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

const ArticleDisplay = () => {
  const local = useLocalSearchParams();
  const articleId = local.articleId;
  const [isModalVisible, setModalVisible] = useState(false);
  const [postSaved, setPostSaved] = useState(false);
  const newsArticle = {
    article_id: "abcd",
    title:
      "Biden seeking re-election in 2024, and his likely opponent is Jeffrey Epstein",
    author: "Lorem Ipsum",
    company: "BBC",
    verified: true,
    live: false,
    image_uri:
      "https://cdn.britannica.com/66/226766-138-235EFD92/who-is-President-Joe-Biden.jpg?w=800&h=450&c=crop",
  };
  const toggleModal = () => {
    setModalVisible(!isModalVisible);
  };

  return (
    <SafeAreaView
      className="bg-white h-full w-full"
      style={{ flex: 1, paddingTop: StatusBar.currentHeight }}
    >
      {articleId == "abcd" ? (
        <ScrollView>
          <View className="flex flex-row px-3 pt-2 items-center">
            <TouchableOpacity onPress={() => router.push("/home")}>
              <LucideChevronLeft size={28} className="text-black" />
            </TouchableOpacity>
            <View className="ml-auto">
              <View className="flex flex-row gap-1">
                <TouchableOpacity onPress={toggleModal}>
                  <LucideSend size={32} className="text-primary" />
                </TouchableOpacity>
                <TouchableOpacity onPress={() => setPostSaved(!postSaved)}>
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
            <View className="flex flex-col gap-1">
              {/* Article title element */}
              <View className="h-44 w-full">
                <Image
                  source={{ uri: newsArticle.image_uri }}
                  className="w-full h-full"
                />
              </View>
            </View>
            <View className="flex flex-col px-3 pt-3">
              <Text className="text-lg font-bold">{newsArticle.title}</Text>
              <View className="flex flex-row w-full items-center gap-3 pt-2">
                <Image
                  source={{
                    uri: "https://t4.ftcdn.net/jpg/06/08/55/73/360_F_608557356_ELcD2pwQO9pduTRL30umabzgJoQn5fnd.jpg",
                  }}
                  className="w-8 h-8 rounded-full"
                />
                <View className="flex flex-row items-center">
                  <Text className="pr-1 text-primary">
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
                <Text className="text-primary">2d</Text>
              </View>
              <Text className="mt-1 text-sm font-light">5-minute read</Text>
              <View className="pt-3">
                <Text>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce
                  sit amet congue nibh. Aenean sit amet justo egestas, feugiat
                  sapien at, mollis odio. Mauris posuere dolor erat, et
                  condimentum quam ullamcorper at. Phasellus ultrices est ante,
                  eu placerat velit lacinia id. Nulla eget nibh ut magna
                  efficitur finibus vitae eu ligula. Integer a leo sapien.
                  Aliquam elit sapien, egestas vulputate erat vitae, interdum
                  consectetur nunc. Sed eu tincidunt nibh. Maecenas sed eros ac
                  leo tincidunt laoreet. Fusce lectus nisi, rhoncus quis
                  vulputate vel, feugiat nec tellus. Nam interdum, quam ut
                  egestas ultricies, ipsum arcu vestibulum neque, volutpat
                  ultricies augue dolor at mi. Donec non sem rhoncus, feugiat
                  erat sed, tincidunt arcu. Nulla facilisi. Aliquam faucibus
                  hendrerit sapien sit amet egestas. Etiam finibus mauris
                  laoreet purus malesuada euismod. Fusce tempus sollicitudin
                  tortor, sit amet elementum risus vehicula ut. Vivamus ut
                  facilisis massa. Maecenas sit amet diam quis urna vestibulum
                  venenatis. Nulla arcu diam, egestas sit amet tincidunt ac,
                  euismod sollicitudin massa. Phasellus a augue arcu. Curabitur
                  lobortis metus sed arcu euismod fermentum. Fusce cursus, lacus
                  eget convallis sagittis, lacus erat pharetra mauris, nec
                  vestibulum diam arcu non justo. Sed nec pretium nunc. Donec a
                  tempor sem. Maecenas et posuere ipsum. Aenean ullamcorper sit
                  amet nulla vitae pellentesque. Lorem ipsum dolor sit amet,
                  consectetur adipiscing elit. Fusce sit amet congue nibh.
                  Aenean sit amet justo egestas, feugiat sapien at, mollis odio.
                  Mauris posuere dolor erat, et condimentum quam ullamcorper at.
                  Phasellus ultrices est ante, eu placerat velit lacinia id.
                  Nulla eget nibh ut magna efficitur finibus vitae eu ligula.
                  Integer a leo sapien. Aliquam elit sapien, egestas vulputate
                  erat vitae, interdum consectetur nunc. Sed eu tincidunt nibh.
                  Maecenas sed eros ac leo tincidunt laoreet. Fusce lectus nisi,
                  rhoncus quis vulputate vel, feugiat nec tellus. Nam interdum,
                  quam ut egestas ultricies, ipsum arcu vestibulum neque,
                  volutpat ultricies augue dolor at mi. Donec non sem rhoncus,
                  feugiat erat sed, tincidunt arcu. Nulla facilisi. Aliquam
                  faucibus hendrerit sapien sit amet egestas. Etiam finibus
                  mauris laoreet purus malesuada euismod. Fusce tempus
                  sollicitudin tortor, sit amet elementum risus vehicula ut.
                  Vivamus ut facilisis massa. Maecenas sit amet diam quis urna
                  vestibulum venenatis. Nulla arcu diam, egestas sit amet
                  tincidunt ac, euismod sollicitudin massa. Phasellus a augue
                  arcu. Curabitur lobortis metus sed arcu euismod fermentum.
                  Fusce cursus, lacus eget convallis sagittis, lacus erat
                  pharetra mauris, nec vestibulum diam arcu non justo. Sed nec
                  pretium nunc. Donec a tempor sem. Maecenas et posuere ipsum.
                  Aenean ullamcorper sit amet nulla vitae pellentesque.
                </Text>
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
      ) : (
        <ScrollView>
          <View className="flex flex-row px-3 pt-2 items-center">
            <TouchableOpacity onPress={() => router.push("/home")}>
              <LucideChevronLeft size={28} className="text-black" />
            </TouchableOpacity>
          </View>
          <View className="flex justify-center items-center">
            <Text>This article does not exist (debugId: {articleId})</Text>
          </View>
        </ScrollView>
      )}

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
};

export default ArticleDisplay;
