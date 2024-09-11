import {
  View,
  Text,
  SafeAreaView,
  Image,
  ScrollView,
  TouchableOpacity,
  Switch,
  StyleSheet,
  Linking,
} from "react-native";
import React, { useState } from "react";
import images from "../../constants/images";
import { LucideChevronRight, LucideFeather } from "lucide-react-native";

const Settings = () => {
  const [form, setForm] = useState({
    emailNotifications: true,
    pushNotifications: false,
  });
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
          <Text className="text-2xl font-bold mb-3">Settings</Text>
        </View>

        <ScrollView
          contentContainerStyle={styles.content}
          showsVerticalScrollIndicator={false}
        >
          <View className="flex flex-col">
            <Text className="m-2 ml-3 uppercase text-[#a69f9f] font-semibold">
              Account
            </Text>
            <View style={styles.sectionBody}>
              <TouchableOpacity
                onPress={() => {
                  // handle onPress
                }}
                className="bg-white flex flex-row p-3 items-center rounded-2xl"
              >
                <Image
                  alt=""
                  source={{
                    uri: "https://t4.ftcdn.net/jpg/06/08/55/73/360_F_608557356_ELcD2pwQO9pduTRL30umabzgJoQn5fnd.jpg",
                  }}
                  className="w-16 h-16 rounded-full mr-3"
                />
                <View className="flex flex-col justify-center mr-auto">
                  <Text className="text-lg font-semibold">John Doe</Text>
                  <Text className="text-base text-[#858585]">
                    john@example.com
                  </Text>
                </View>
                <LucideChevronRight color="#bcbcbc" size={22} />
              </TouchableOpacity>
            </View>
          </View>
          <View className="flex flex-col mt-3">
            <Text className="m-2 ml-3 uppercase text-[#a69f9f] font-semibold">
              Preferences
            </Text>
            <View style={styles.sectionBody}>
              <View className="pl-4 bg-white border-t rounded-t-xl border-[#f0f0f0]">
                <TouchableOpacity
                  onPress={() => {
                    alert(
                      "English is the only language offered at the moment!",
                    );
                  }}
                  style={styles.row}
                >
                  <Text style={styles.rowLabel}>Language</Text>
                  <View style={styles.rowSpacer} />
                  <Text style={styles.rowValue}>English</Text>
                  <LucideChevronRight color="#bcbcbc" size={19} />
                </TouchableOpacity>
              </View>

              <View className="pl-4 bg-white border-t rounded-b-xl border-[#f0f0f0]">
                <View style={styles.row}>
                  <Text style={styles.rowLabel}>Push Notifications</Text>
                  <View style={styles.rowSpacer} />
                  <Switch
                    onValueChange={(pushNotifications) =>
                      setForm({ ...form, pushNotifications })
                    }
                    style={{
                      transform: [{ scaleX: 0.95 }, { scaleY: 0.95 }],
                    }}
                    value={form.pushNotifications}
                  />
                </View>
              </View>
            </View>
          </View>
          <View className="flex flex-col mt-3">
            <Text className="m-2 ml-3 uppercase text-[#a69f9f] font-semibold">
              Resources
            </Text>
            <View style={styles.sectionBody}>
              <View className="pl-4 bg-white border-t rounded-t-xl border-[#f0f0f0]">
                <TouchableOpacity
                  onPress={() => {
                    // Linking.openURL("mailto:luciano.suen@online.island.edu.hk");
                    alert("Contact luciano.suen@online.island.edu.hk");
                  }}
                  style={styles.row}
                >
                  <Text style={styles.rowLabel}>Contact Us</Text>
                  <View style={styles.rowSpacer} />
                  <LucideChevronRight color="#bcbcbc" size={19} />
                </TouchableOpacity>
              </View>
              <View className="pl-4 bg-white border-t border-[#f0f0f0]">
                <TouchableOpacity
                  onPress={() => {
                    alert("Contact luciano.suen@online.island.edu.hk");
                  }}
                  style={styles.row}
                >
                  <Text style={styles.rowLabel}>Report Bug</Text>
                  <View style={styles.rowSpacer} />
                  <LucideChevronRight color="#bcbcbc" size={19} />
                </TouchableOpacity>
              </View>
              <View className="pl-4 bg-white border-t border-[#f0f0f0]">
                <TouchableOpacity
                  onPress={() => {
                    // handle onPress
                  }}
                  style={styles.row}
                >
                  <Text style={styles.rowLabel}>Rate in App Store</Text>
                  <View style={styles.rowSpacer} />
                  <LucideChevronRight color="#bcbcbc" size={19} />
                </TouchableOpacity>
              </View>
              <View className="pl-4 bg-white border-t rounded-b-xl border-[#f0f0f0]">
                <TouchableOpacity
                  onPress={() => {
                    // handle onPress
                  }}
                  style={styles.row}
                >
                  <Text style={styles.rowLabel}>Terms and Privacy</Text>
                  <View style={styles.rowSpacer} />
                  <LucideChevronRight color="#bcbcbc" size={19} />
                </TouchableOpacity>
              </View>
            </View>
          </View>
          <View className="flex flex-col mt-3">
            <View style={styles.sectionBody}>
              <View className="pl-4 bg-white border-t rounded-xl mb-1 border-[#f0f0f0]">
                <TouchableOpacity
                  onPress={() => {
                    // handle onPress
                  }}
                  style={styles.row}
                >
                  <Text style={[styles.rowLabel, styles.rowLabelLogout]}>
                    Reset user data
                  </Text>
                </TouchableOpacity>
              </View>
              <View
                className="pl-4 bg-white border-t rounded-xl border-[#f0f0f0]"
                style={{ alignItems: "center" }}
              >
                <TouchableOpacity
                  onPress={() => {
                    // handle onPress
                  }}
                  style={styles.row}
                >
                  <Text style={[styles.rowLabel, styles.rowLabelLogout]}>
                    Log out
                  </Text>
                </TouchableOpacity>
              </View>
            </View>
          </View>
          <Text style={styles.contentFooter}>App Version 2.24 #50491</Text>
          <View className="h-[125px]" />
        </ScrollView>
      </View>
    </SafeAreaView>
  );
};
const styles = StyleSheet.create({
  /** Header */
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    width: "100%",
    paddingHorizontal: 16,
  },
  headerAction: {
    width: 40,
    height: 40,
    alignItems: "flex-start",
    justifyContent: "center",
  },
  headerTitle: {
    fontSize: 19,
    fontWeight: "600",
    color: "#000",
    flexGrow: 1,
    flexShrink: 1,
    flexBasis: 0,
    textAlign: "center",
  },
  /** Content */
  content: {
    paddingHorizontal: 16,
  },
  contentFooter: {
    marginTop: 24,
    fontSize: 13,
    fontWeight: "500",
    textAlign: "center",
    color: "#a69f9f",
  },
  /** Section */
  section: {
    paddingVertical: 12,
  },
  sectionBody: {
    borderRadius: 12,
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.2,
    shadowRadius: 1.41,
    elevation: 2,
  },
  /** Profile */
  profile: {
    padding: 12,
    backgroundColor: "#fff",
    borderRadius: 12,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "flex-start",
  },
  profileAvatar: {
    width: 60,
    height: 60,
    borderRadius: 9999,
    marginRight: 12,
  },
  profileName: {
    fontSize: 18,
    fontWeight: "600",
    color: "#292929",
  },
  profileHandle: {
    marginTop: 2,
    fontSize: 16,
    fontWeight: "400",
    color: "#858585",
  },
  /** Row */
  row: {
    height: 44,
    width: "100%",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "flex-start",
    paddingRight: 12,
  },
  rowWrapper: {
    paddingLeft: 16,
    backgroundColor: "#fff",
    borderTopWidth: 1,
    borderColor: "#f0f0f0",
  },
  rowLabel: {
    fontSize: 16,
    letterSpacing: 0.24,
    color: "#000",
  },
  rowSpacer: {
    flexGrow: 1,
    flexShrink: 1,
    flexBasis: 0,
  },
  rowValue: {
    fontSize: 16,
    fontWeight: "500",
    color: "#ababab",
    marginRight: 4,
  },
  rowLabelLogout: {
    width: "100%",
    textAlign: "center",
    fontWeight: "600",
    color: "#dc2626",
  },
});
export default Settings;
