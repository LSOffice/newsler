import { View, Text } from "react-native";
import React from "react";
import { Slot, Stack } from "expo-router";
import { NativeWindStyleSheet } from "nativewind";
import Toast from "react-native-toast-message";

NativeWindStyleSheet.setOutput({
  default: "native",
});

const RootLayout = () => {
  return (
    <>
      <Stack screenOptions={{ animation: "fade_from_bottom" }}>
        <Stack.Screen
          name="index"
          options={{ headerShown: false, gestureEnabled: false }}
        />
        <Stack.Screen name="(auth)" options={{ headerShown: false }} />
        <Stack.Screen
          name="(tabs)"
          options={{ headerShown: false, gestureEnabled: false }}
        />

        <Stack.Screen
          name="(article)/article/index"
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="(article)/article/[articleId]/index"
          options={{ headerShown: false }}
        />
      </Stack>
      <Toast />
    </>
  );
};

export default RootLayout;
