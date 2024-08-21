import { View, Text, ScrollView, FlatList, ActivityIndicator, Image, TouchableOpacity } from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context';
import React, { useEffect, useState } from 'react'
import images from '../../constants/images';
import { Bell, LucideBell, LucideLocate, LucideMenu, LucideUser, LucideVerified, UserCheck, UserX } from 'lucide-react-native';
import BlinkDot from '../../components/Blink';
import Explore from './explore';
import Saved from './saved';
import Settings from './settings';
import HorizontalScrollMenu, { RouteProps } from '@nyashanziramasanga/react-native-horizontal-scroll-menu/src';
import { router } from 'expo-router';

const Home = () => {
  const loading = React.useRef(false)
  const [dataSource, setDataSource] = useState([{}])
  const [offset, setOffset] = useState(1)
  const [isListEnd, setIsListEnd] = useState(false)
  const [selectedIndex, setSelectedIndex] = useState(0)
  const [yOffset, setyOffset] = useState(0)
  const isReload = React.useRef(false)

  useEffect(() => {
    getData()
  }, [])

  const numOfTabs = 4
  const NavigationTabs = [
    {
      id: 0,
      name: 'Trending',
    },
    {
      id: 1,
      name: 'Hong Kong',
    },
    {
      id: 2,
      name: 'Sports',
    },
    {
      id: 3,
      name: 'Politics',
    },
    {
      id: 4,
      name: 'Pop Culture',
    },
  ]

  const newsArticles = [
    {
      id: 'abcd',
      title: 'Biden seeking re-election in 2024',
      author: 'Lorem Ipsum',
      company: 'BBC',
      verified: true,
      image_uri: 'https://www.usatoday.com/gcdn/authoring/authoring-images/2024/07/05/PMJS/74313173007-biden-madison.jpg?crop=8255,4645,x0,y429&width=660&height=371&format=pjpg&auto=webp'
    },
    {
      id: 'abcde',
      title: 'GTA VI Trailer out: Much to look forward to?',
      author: 'Jeff Bob',
      company: 'Tailor News',
      verified: false,
      image_uri: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVA7faN3W4oHcL_WF5sUYtMdBDjMld_erQuQ&s'
    },
    {
      id: 'abcde',
      title: 'GTA VI Trailer out: Much to look forward to?',
      author: 'Jeff Bob',
      company: 'Tailor News',
      verified: false,
      image_uri: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVA7faN3W4oHcL_WF5sUYtMdBDjMld_erQuQ&s'
    },
    {
      id: 'abcde',
      title: 'GTA VI Trailer out: Much to look forward to?',
      author: 'Jeff Bob',
      company: 'Tailor News',
      verified: false,
      image_uri: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVA7faN3W4oHcL_WF5sUYtMdBDjMld_erQuQ&s'
    },
    {
      id: 'abcde',
      title: 'GTA VI Trailer out: Much to look forward to?',
      author: 'Jeff Bob',
      company: 'Tailor News',
      verified: false,
      image_uri: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVA7faN3W4oHcL_WF5sUYtMdBDjMld_erQuQ&s'
    },
    {
      id: 'abcde',
      title: 'GTA VI Trailer out: Much to look forward to?',
      author: 'Jeff Bob',
      company: 'Tailor News',
      verified: false,
      image_uri: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVA7faN3W4oHcL_WF5sUYtMdBDjMld_erQuQ&s'
    }
  ]

  const onPress = (route: RouteProps) => {
    setSelectedIndex(route.id)
    console.log('Tab pressed', route)
  }
  
  const getData = () => {
    console.log('getting data')
    if ((!loading.current && !isListEnd) || isReload.current) {
      if (!isReload.current) {
        loading.current = true
      }
      setDataSource([])
      
      fetch('https://dummyjson.com/products?offset=' + offset)
        .then(response => response.json())
        .then(data => {
          if (isReload.current) {
            isReload.current = false
          }
          if (data.products.length > 0) {
            setOffset(offset + 1)
            setDataSource([...newsArticles])
            loading.current = false
            
          }
          else {
            setIsListEnd(true)
            loading.current = false
          }
        })
        .catch(error => {
          console.error(error)
        })
    }
  }

  const renderFooter = () => {
    return (
      <View>
        {loading.current ? (
          <ActivityIndicator color='black' className='m-14' />
        ) : null}
      </View>
    )
  }

  const ItemView = ({ item }: {
    item: {
      author: string,
      company: string,
      image_uri: string,
      title: string,
      verified: boolean,
      article_id: string
    }
  }) => {
    return (
      <TouchableOpacity onPress={() => getItem(item)} className='border-[0.5px] rounded-2xl border-tertiary flex flex-col h-48'>
        <View className='h-3/4'>
          <Image
            source={{uri: item.image_uri}}
            className='w-full h-full rounded-t-2xl'
          />
        </View>
        <View className='h-1/4 bg-gray-200 rounded-b-2xl px-3 flex flex-col justify-center'>
          <Text numberOfLines={1} className='text-base font-medium'>{item.title}</Text>
          <View className='flex flex-row gap-1 items-center'>
            <Text className='text-xs font-light'>By {item.author}, {item.company}</Text>
            {item.verified ? <UserCheck size={14} className='text-primary'/> : <UserX size={14} className='text-black'/>}
          </View>
        </View>
      </TouchableOpacity>
      
    )
  }

  const ItemSeperatorView = () => {
    return (
      <View className='h-5'>

      </View>
    )
  }

  const getItem = ( item : {
    author: string,
    company: string,
    image_uri: string,
    title: string,
    verified: boolean,
    article_id: string
  }) => {
    alert(JSON.stringify(item))
    //router.push('/article/' + item.article_id)
  }

  const handleScrollToTop = (e) => {
    if (yOffset <= 0 && e.nativeEvent.contentOffset.y > 0) {
      // When user is just normally scrolling
    } else if (yOffset > 0 && e.nativeEvent.contentOffset.y <= 0){
      if (!loading.current) {
        isReload.current = true
        getData()
      }
    }
    setyOffset(e.nativeEvent.contentOffset.y)
  }

  return (
    <SafeAreaView className='bg-white h-full w-full flex-1'>
      <View className='flex flex-col gap-3 mb-2'>
        <View className='border-b-[0.5px] py-2 border-tertiary px-4'>
          <View className='flex flex-row w-full justify-center items-center'>
            <TouchableOpacity className='mr-auto' onPress={() => {}}>
              <LucideMenu size={32} className='text-primary'/>
            </TouchableOpacity>
            
            <View className='flex flex-row items-center gap-2 justify-center'>
              <Image
                source={images.logo}
                className='w-10 h-10'
                resizeMode='contain'
              />
              <Text className='text-2xl text-primary font-bold text-center'>Newsler</Text>
            </View>
            <TouchableOpacity className='ml-auto' onPress={() => {}}>
              <LucideBell size={32} className='text-primary'/>
            </TouchableOpacity>
          </View>
        </View>
        {/* <View className='flex flex-col px-4'>
          <View className='rounded-xl flex flex-row items-center'>
            <BlinkDot duration={2000}>
              <View className='rounded-2xl w-3 h-3 bg-secondary'/>
            </BlinkDot>
            <LucideLocate size={20} className='text-secondary mr-1.5'/>
            <Text className='text-xs'>Your approx. location is used</Text>
          </View>
        </View> */}
        <HorizontalScrollMenu
          items={NavigationTabs}
          onPress={onPress}
          selected={selectedIndex}
          activeBackgroundColor={`${selectedIndex == 0 ? '#FCA311' : '#275F6F'}`}
          activeTextColor={`${selectedIndex == 0 ? 'black' : 'white'}`}
          buttonStyle={{ 
            borderColor: 'white',
          }}
          textStyle={{
            color: '#275F6F'
          }}
        />
        
      </View>
      
      {
        <View>
          {isReload.current ? (
            <ActivityIndicator color='black' className='mb-3' />
          ) : null}
        </View>
      }

      <FlatList 
        data={dataSource}
        keyExtractor={(item, index) => index.toString()}
        ItemSeparatorComponent={ItemSeperatorView}
        renderItem={ItemView}
        ListFooterComponent={renderFooter}
        onEndReached={getData}
        onEndReachedThreshold={0.5}
        className='px-4'
        onScroll={handleScrollToTop}
      />
    </SafeAreaView>
  )
}

export default Home
