import { View, Text } from "react-native";
import React from "react";
import { Slot, Stack } from "expo-router";
import { NativeWindStyleSheet } from "nativewind";
import Toast from "react-native-toast-message";

// tailwind react native version init
NativeWindStyleSheet.setOutput({
  default: "native",
});

const RootLayout = () => {
  return (
    <>
      {/* stack navigator for the entire app */}
      <Stack screenOptions={{ animation: "fade_from_bottom" }}>
        {/* index screen,  header is hidden and gestures are disabled */}
        <Stack.Screen
          name="index"
          options={{ headerShown: false, gestureEnabled: false }}
        />
        {/* authentication stack, header is hidden */}
        <Stack.Screen name="(auth)" options={{ headerShown: false }} />
        {/* tabs navigator, header is hidden and gestures are disabled */}
        <Stack.Screen
          name="(tabs)"
          options={{ headerShown: false, gestureEnabled: false }}
        />
        {/* education stack, header is hidden */}
        <Stack.Screen name="(education)" options={{ headerShown: false }} />
        {/* article stack, header is hidden */}
        <Stack.Screen
          name="(article)/article/index"
          options={{ headerShown: false }}
        />
        {/* article details screen, header is hidden and gestures are disabled */}
        <Stack.Screen
          name="(article)/article/[articleId]/index"
          options={{ headerShown: false, gestureEnabled: false }}
        />
      </Stack>
      <Toast />
    </>
  );
};

export default RootLayout;
