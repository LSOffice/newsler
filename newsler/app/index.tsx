// this file returns the main page
// path: /

import { Redirect, router } from "expo-router";
import React, { useEffect } from "react";
import {
  View,
  Text,
  ScrollView,
  Image,
  Button,
  TouchableOpacity,
  TextInput,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import images from "../constants/images";
import { StatusBar } from "expo-status-bar";
import { NativeWindStyleSheet } from "nativewind";
import AsyncStorage from "@react-native-async-storage/async-storage";
import Toast from "react-native-toast-message";

interface TextWithDefaultProps extends Text {
  defaultProps?: { allowFontScaling?: boolean };
}

interface TextInputWithDefaultProps extends TextIput {
  defaultProps?: { allowFontScaling?: boolean };
}

(Text as unknown as TextWithDefaultProps).defaultProps =
  (Text as unknown as TextWithDefaultProps).defaultProps || {};
(Text as unknown as TextWithDefaultProps).defaultProps!.allowFontScaling =
  false;
(TextInput as unknown as TextInputWithDefaultProps).defaultProps =
  (TextInput as unknown as TextInputWithDefaultProps).defaultProps || {};
(
  TextInput as unknown as TextInputWithDefaultProps
).defaultProps!.allowFontScaling = false;

export default function App() {
  //this function fetches the userId from AsyncStorage and redirects to the login page if it exists.
  useEffect(() => {
    const fetchUserId = async () => {
      const userId = await AsyncStorage.getItem("userId");
      if (userId !== null) {
        router.push("/login");
      }
    };

    const result = fetchUserId().catch(console.error);
  });

  //this is the main UI of the app.
  return (
    <SafeAreaView className="bg-white h-full">
      <ScrollView contentContainerStyle={{ height: "100%", width: "100%" }}>
        <View className="w-full justify-center items-center min-h-[90vh] px-4 flex flex-col">
          <View className="flex flex-col gap-2 justify-center items-center">
            <View className="flex flex-row items-center justify-center gap-2">
              <Image
                source={images.logo}
                className="w-16 h-16"
                resizeMode="contain"
              />
              <Text className="text-3xl text-primary font-bold text-center">
                Newsler
              </Text>
            </View>
            <View className="flex flex-col justify-center items-center">
              <Text className="text-2xl text-center font-medium">
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
            className={`bg-primary rounded-xl h-10 justify-center items-center w-full absolute bottom-0`}
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
