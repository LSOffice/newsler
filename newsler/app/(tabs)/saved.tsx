import { View, Text, Image, ScrollView } from "react-native";
import React, { useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import images from "../../constants/images";

const Saved = () => {
  const [savedPosts, setSavedPosts] = useState([]);
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

        <View className="flex flex-col px-4 mt-3">
          <Text className="text-2xl font-bold mb-3">Saved Articles</Text>
          <ScrollView showsVerticalScrollIndicator={false}>
            <View className="flex flex-row">
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
            </View>
            <View className="flex flex-row">
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
            </View>
            <View className="flex flex-row">
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
            </View>
            <View className="flex flex-row">
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
            </View>
            <View className="flex flex-row">
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
            </View>
            <View className="flex flex-row">
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
            </View>
            <View className="flex flex-row">
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
            </View>
            <View className="flex flex-row">
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
              <View className="w-1/4 h-24 border"></View>
            </View>
            <View className="h-[150px]" />
          </ScrollView>
        </View>
      </View>
    </SafeAreaView>
  );
};

export default Saved;
