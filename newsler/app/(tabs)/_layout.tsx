import { Tabs } from "expo-router";
import {
  Bookmark,
  GraduationCap,
  Home,
  LucideIcon,
  Search,
  Settings,
} from "lucide-react-native";
import React, { ReactElement } from "react";
import { View, Text, Image } from "react-native";
import Education from "./edu";

interface TabIconProps {
  icon: ReactElement;
  color: string;
  focused: Boolean;
}

const TabIcon: React.FC<TabIconProps> = ({ icon, color, focused }) => {
  return <View className="item-center justify-center gap-2">{icon}</View>;
};

const TabsLayout = () => {
  return (
    <Tabs
      screenOptions={{
        tabBarShowLabel: false,
        tabBarActiveTintColor: "#FCA311",
        tabBarInactiveTintColor: "#275F6F",
        tabBarStyle: {
          backgroundColor: "#FFFFFF",
          borderTopWidth: 0.5,
          borderTopColor: "#D3D3D3",
          height: 70,
        },
        animation: "shift",
      }}
    >
      <Tabs.Screen
        name="edu"
        options={{
          title: "Edu",
          headerShown: false,
          tabBarIcon: ({ color, focused }) => (
            <TabIcon
              icon={
                <GraduationCap
                  className={`${focused ? `text-secondary` : `text-primary`}`}
                />
              }
              color={color}
              focused={focused}
            />
          ),
        }}
      />

      <Tabs.Screen
        name="home"
        options={{
          title: "Home",
          headerShown: false,
          tabBarIcon: ({ color, focused }) => (
            <TabIcon
              icon={
                <Home
                  className={`${focused ? `text-secondary` : `text-primary`}`}
                />
              }
              color={color}
              focused={focused}
            />
          ),
        }}
      />
      <Tabs.Screen
        name="saved"
        options={{
          title: "Saved",
          headerShown: false,
          tabBarIcon: ({ color, focused }) => (
            <TabIcon
              icon={
                <Bookmark
                  className={`${focused ? `text-secondary` : `text-primary`}`}
                />
              }
              color={color}
              focused={focused}
            />
          ),
        }}
      />
      <Tabs.Screen
        name="settings"
        options={{
          title: "Settings",
          headerShown: false,
          tabBarIcon: ({ color, focused }) => (
            <TabIcon
              icon={
                <Settings
                  className={`${focused ? `text-secondary` : `text-primary`}`}
                />
              }
              color={color}
              focused={focused}
            />
          ),
        }}
      />
    </Tabs>
  );
};

export default TabsLayout;
