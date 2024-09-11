import { Redirect, router } from "expo-router";
import React from "react";
import {
  View,
  Text,
  ScrollView,
  Image,
  Button,
  TouchableOpacity,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import images from "../constants/images";
import { StatusBar } from "expo-status-bar";

export default function App() {
  return (
    <SafeAreaView className="bg-white h-full">
      <ScrollView contentContainerStyle={{ height: "100%", width: "100%" }}>
        <View className="w-full justify-center items-center min-h-[90vh] px-4 flex flex-col">
          <View className="flex flex-col gap-2 justify-center items-center">
            <View className="flex flex-row items-center justify-center gap-2">
              <Image
                source={images.logo}
                className="w-14 h-14"
                resizeMode="contain"
              />
              <Text className="text-3xl text-primary font-bold text-center">
                Newsler
              </Text>
            </View>
            <View className="flex flex-col justify-center items-center">
              <Text className="text-xl text-center font-medium">
                News reimagined, modernised
              </Text>
              <Text className="text-xl text-center font-medium">
                exclusively on{" "}
                <Text className="text-xl font-medium text-primary">
                  Newsler
                </Text>
              </Text>
            </View>
          </View>

          <TouchableOpacity
            activeOpacity={0.7}
            onPress={() => router.push("/signup")}
            className={`bg-primary rounded-xl h-10 justify-center items-center w-full mt-5`}
          >
            <Text className="text-white font-semibold text-lg">
              Sign up with email
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>

      <StatusBar backgroundColor={"#275F6F"} style={"light"} />
    </SafeAreaView>
  );
}
