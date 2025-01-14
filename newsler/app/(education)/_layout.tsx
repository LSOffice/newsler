import { View, Text } from "react-native";
import React from "react";
import { Stack } from "expo-router";
import { NavigationContainer } from "@react-navigation/native";

const EducationLayout = () => {
  return (
    <NavigationContainer>
      <Stack>
        <Stack.Screen
          name="classroom"
          options={{
            headerShown: false,
          }}
        />
        <Stack.Screen
          name="assignment"
          options={{
            headerShown: false,
          }}
        />
      </Stack>
    </NavigationContainer>
  );
};

export default EducationLayout;
