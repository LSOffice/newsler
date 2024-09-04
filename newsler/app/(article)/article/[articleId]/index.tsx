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
} from "react-native";
import React from "react";
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
  LucideHeart,
  LucideUpload,
  LucideUserCheck,
  LucideUserX,
} from "lucide-react-native";

const ArticleDisplay = () => {
  const local = useLocalSearchParams();
  const articleId = local.articleId;
  const newsArticle = {
    article_id: "abcd",
    title:
      "Biden seeking re-election in 2024, and his likely opponent is Jeffrey Epstein",
    author: "Lorem Ipsum",
    company: "BBC",
    verified: true,
    live: false,
    image_uri:
      "https://www.usatoday.com/gcdn/authoring/authoring-images/2024/07/05/PMJS/74313173007-biden-madison.jpg?crop=8255,4645,x0,y429&width=660&height=371&format=pjpg&auto=webp",
  };

  return (
    <SafeAreaView
      className="bg-white h-full w-full"
      style={{ flex: 1, paddingTop: StatusBar.currentHeight }}
    >
      <ScrollView>
        <View className="flex flex-row px-3 pt-2 items-center">
          <TouchableOpacity onPress={() => router.push("/home")}>
            <LucideChevronLeft size={28} className="text-black" />
          </TouchableOpacity>
          <View className="ml-auto">
            <View className="flex flex-row gap-1">
              <TouchableOpacity>
                <LucideBookmark size={32} className="text-primary" />
              </TouchableOpacity>
              <TouchableOpacity>
                <LucideUpload size={32} className="text-primary" />
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
            <View className="pt-3">
              <Text>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce
                sit amet congue nibh. Aenean sit amet justo egestas, feugiat
                sapien at, mollis odio. Mauris posuere dolor erat, et
                condimentum quam ullamcorper at. Phasellus ultrices est ante, eu
                placerat velit lacinia id. Nulla eget nibh ut magna efficitur
                finibus vitae eu ligula. Integer a leo sapien. Aliquam elit
                sapien, egestas vulputate erat vitae, interdum consectetur nunc.
                Sed eu tincidunt nibh. Maecenas sed eros ac leo tincidunt
                laoreet. Fusce lectus nisi, rhoncus quis vulputate vel, feugiat
                nec tellus. Nam interdum, quam ut egestas ultricies, ipsum arcu
                vestibulum neque, volutpat ultricies augue dolor at mi. Donec
                non sem rhoncus, feugiat erat sed, tincidunt arcu. Nulla
                facilisi. Aliquam faucibus hendrerit sapien sit amet egestas.
                Etiam finibus mauris laoreet purus malesuada euismod. Fusce
                tempus sollicitudin tortor, sit amet elementum risus vehicula
                ut. Vivamus ut facilisis massa. Maecenas sit amet diam quis urna
                vestibulum venenatis. Nulla arcu diam, egestas sit amet
                tincidunt ac, euismod sollicitudin massa. Phasellus a augue
                arcu. Curabitur lobortis metus sed arcu euismod fermentum. Fusce
                cursus, lacus eget convallis sagittis, lacus erat pharetra
                mauris, nec vestibulum diam arcu non justo. Sed nec pretium
                nunc. Donec a tempor sem. Maecenas et posuere ipsum. Aenean
                ullamcorper sit amet nulla vitae pellentesque. Lorem ipsum dolor
                sit amet, consectetur adipiscing elit. Fusce sit amet congue
                nibh. Aenean sit amet justo egestas, feugiat sapien at, mollis
                odio. Mauris posuere dolor erat, et condimentum quam ullamcorper
                at. Phasellus ultrices est ante, eu placerat velit lacinia id.
                Nulla eget nibh ut magna efficitur finibus vitae eu ligula.
                Integer a leo sapien. Aliquam elit sapien, egestas vulputate
                erat vitae, interdum consectetur nunc. Sed eu tincidunt nibh.
                Maecenas sed eros ac leo tincidunt laoreet. Fusce lectus nisi,
                rhoncus quis vulputate vel, feugiat nec tellus. Nam interdum,
                quam ut egestas ultricies, ipsum arcu vestibulum neque, volutpat
                ultricies augue dolor at mi. Donec non sem rhoncus, feugiat erat
                sed, tincidunt arcu. Nulla facilisi. Aliquam faucibus hendrerit
                sapien sit amet egestas. Etiam finibus mauris laoreet purus
                malesuada euismod. Fusce tempus sollicitudin tortor, sit amet
                elementum risus vehicula ut. Vivamus ut facilisis massa.
                Maecenas sit amet diam quis urna vestibulum venenatis. Nulla
                arcu diam, egestas sit amet tincidunt ac, euismod sollicitudin
                massa. Phasellus a augue arcu. Curabitur lobortis metus sed arcu
                euismod fermentum. Fusce cursus, lacus eget convallis sagittis,
                lacus erat pharetra mauris, nec vestibulum diam arcu non justo.
                Sed nec pretium nunc. Donec a tempor sem. Maecenas et posuere
                ipsum. Aenean ullamcorper sit amet nulla vitae pellentesque.
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
    </SafeAreaView>
  );
};

export default ArticleDisplay;
